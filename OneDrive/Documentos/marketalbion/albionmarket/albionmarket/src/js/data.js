const traerAlbion = 'https://www.albion-online-data.com/api/v2/stats/history/T4_BAG?date=2-5-2020&end_date=2-12-2020&locations=Caerleon&qualities=2&time-scale=6' ; 

export const data = async() => {
    await fetch(traerAlbion)
        .then(resp => resp.json())
        .then(console.log);
}
