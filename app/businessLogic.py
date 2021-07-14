from app import app, db
from app.models import Supply
import datetime

def averageCalculation(result):

    avg_calc = 0
    fullTank = result.get('fullTank')

    if fullTank:

        carId = result.get('carId')
        supplyDate = result.get('supplyDate')

        supsCurrentMonth = Supply.query.filter(Supply.carId == carId).order_by(Supply.id.desc())

        if supsCurrentMonth.filter(Supply.fullTank == True).count() >= 1 and supplyDate[0:10] == datetime.date.today().strftime("%Y-%m-%d"):

            totalKm = result.get('totalKm')
            liters = result.get('liters')

            for supply in supsCurrentMonth:
                if supply.fullTank:

                    totalKm = totalKm - supply.totalKm
                    break
                else:
                    liters = liters + supply.liters

            avg_calc = round((100 * liters) / totalKm, 2)

            app.logger.info('Creating Average liter: %s totalKm: %s, average: %s', liters, totalKm, avg_calc)


        # if supsCurrentMonth.filter(Supply.supplyDate >= supplyDate[0:7] + '-01' ).count() >= 1:

    

    return avg_calc