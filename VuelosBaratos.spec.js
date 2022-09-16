import { test, expect } from '@playwright/test';
let fs = require('fs');
const { GoogleFlightsPage } = require('C:/Users/octi1/OneDrive/Escritorio/Codigo/Vuelos Baratos/GoogleFlightsPage');
const { GraficoDePreciosPage } = require('C:/Users/octi1/OneDrive/Escritorio/Codigo/Vuelos Baratos/GraficoDePreciosPage');
//const { Funciones } = require('C:/Users/octi1/OneDrive/Escritorio/Codigo/Vuelos Baratos/Funciones')


test('Entrar al sitio y buscar vuelos baratos', async ({ page }) => {

    //Inicializacion de pagina
    const googleFlightsPage = new GoogleFlightsPage(page);
    const graficoDePreciosPage = new GraficoDePreciosPage(page);
    //const funciones = new Funciones(page);

    //let lista = funciones.getDatos('BUENOSAIRES', 'TOKIO')
    let origen = 'BUENOSAIRES';
    let destino = 'TOKIO';

    //let origen = lista[0];
    //let destino = lista[1];

    await page.goto(`https://www.google.com/travel/flights?q=Flights%20to%20${destino}%20from%20${origen}`);
    
    await expect(page).toHaveTitle(/Flights/);
    
    //Entra al sitio, busca el vuelo y entra al grafico de precios    
    await page.locator(googleFlightsPage.botonGraficoPrecios).nth(1).click();

    //Elige la cantidad el periodo del vuelo ida y vuelta
    for(let i = 0; i<11; i++) {
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