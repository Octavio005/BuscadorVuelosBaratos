import { test, expect } from '@playwright/test';
import fs from 'fs';
import GoogleFlightsPage from './GoogleFlightsPage.mjs';
import GraficoDePreciosPage from './GraficoDePreciosPage.mjs';


test('Entrar al sitio y buscar vuelos baratos', async ({ page }) => {

    //Lectura del json que contiene los datos de las personas
    let content = fs.readFileSync('personas.json', 'utf8');
    const obj = JSON.parse(content);

    //Inicializacion de pagina
    const googleFlightsPage = new GoogleFlightsPage(page);
    const graficoDePreciosPage = new GraficoDePreciosPage(page);

    //Formateo de strings
    obj[0].origen = obj[0].origen.replace(/ /g,'').toUpperCase();
    obj[0].destino = obj[0].destino.replace(/ /g,'').toUpperCase();
    obj[0].dias = parseInt(obj[0].dias);

    
    //Inicio de automatizacion
    await page.goto(`https://www.google.com/travel/flights?q=Flights%20to%20${obj[0].destino}%20from%20${obj[0].origen}`);
    
    await expect(page).toHaveTitle(/Flights/);
    
    //Entra al sitio, busca el vuelo y entra al grafico de precios    
    await page.locator(googleFlightsPage.botonGraficoPrecios).nth(1).click();

    //Elige la cantidad de dias del viaje
    //A obj[0].dias se le resta 4 porque el contador comienza en 4
    for(let i = 0; i<obj[0].dias-4; i++) {
        await page.locator(graficoDePreciosPage.botonSumarDias).click();
    }

    let jsonVuelos = {};
    //Se utiliza un contador para el for ya que al avanzar, sólo se
    //muestran 20 elementos extra
    let indice = 1

    //Toma la fecha y el precio minimo de cada dia
    for(let i = 0; i<13; i++) {
        let lista = await page.locator(graficoDePreciosPage.listaDeVuelos);
        await page.waitForTimeout(2000);
        for(let i = indice; i<61; i++){

            let fechaSinProcesar = '';
            let precio = '';

            await lista.locator(graficoDePreciosPage.barraPrecioDiario + '[' + i + ']').click({force : true});
            if(await page.locator(graficoDePreciosPage.precioDeVuelo).isVisible()){           
                precio = await page.locator(graficoDePreciosPage.precioDeVuelo).textContent();
                fechaSinProcesar = await page.locator(graficoDePreciosPage.fechaDeVuelo).textContent();
            }

            let fecha = fechaSinProcesar.normalize("NFD").replace(/[\u0300-\u036f]/g, '');
            jsonVuelos[fecha] = precio;
        }
        indice = 40
        await page.locator(graficoDePreciosPage.botonSiguienteMes).click();
    }

    jsonVuelos[origen] = destino;

    let jsonString = JSON.stringify(jsonVuelos);
    fs.writeFileSync("Vuelos.json", jsonString, 'UTF-8');

    await page.locator(graficoDePreciosPage.botonAceptar).click();
});
