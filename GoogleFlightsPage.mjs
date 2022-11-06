class GoogleFlightsPage {
    
    vueloOrigen = "//*[@class = 'e5F5td BGeFcf']//*[@jsname = 'pT3pqd']/input";
    vueloDestino = "//*[@class = 'e5F5td vxNK6d']//*[@jsname = 'pT3pqd']/input";
    fechaIda = "//*[@jsname = 'huwV5e']//*[@class = 'GpDmDb q5Vmde']/following-sibling::input";
    fechaVuelta = "//*[@jsname = 'huwV5e']//*[@jscontroller= 's0nXec']/following-sibling::div//input";
    botonBuscar = "//span[text() = 'Buscar']";
    botonGraficoPrecios = "//*[@class = 'IF9f4c']//*[@jsname = 'V67aGc']";
    
    constructor(page) {
        this.page = page;
    }
}

export default GoogleFlightsPage;