class GraficoDePreciosPage {
    
    botonSiguienteMes = "//button[@jsname= 'Oc7uMe']";
    listaDeVuelos = "//*[@series-id]";
    barraPrecioDiario = "//*[@class = 'ZMv3u-JNdkSc ']";
    precioDeVuelo = "//*[@jsname = 'X8UIGb']//*[@class ='YMlIz']";
    fechaDeVuelo = "//*[@jsname = 'X8UIGb']//*[contains(text(), ' - ')]"
    mensajeVuelosNoDisponibles = "//*[@jsname = 'X8UIGb']//*[@class ='tgn7Yd sSHqwe']"
    botonSumarDias = ".yPvl9b > span:nth-child(2) button";
    botonAceptar = "//span[text() = 'OK']";
    
    constructor(page) {
        this.page = page;
    }
}

export default GraficoDePreciosPage;