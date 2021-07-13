from app import app, db
from app.models import Supply


def averageCalculation(result):

    avg_calc = 0
    carId = result.get('carId')
    totalKm = result.get('totalKm')
    liters = result.get('liters')
    fullTank = result.get('fullTank')

    if fullTank:

        supsCurrentMonth = Supply.query.filter_by(carId=carId).order_by(Supply.id.desc())

        if supsCurrentMonth.filter_by(fullTank=True).count() >= 1:
            for supply in supsCurrentMonth:
                if supply.fullTank:

                    totalKm = totalKm - supply.totalKm
                    break
                else:
                    liters = liters + supply.liters

            avg_calc = round((100 * liters) / totalKm, 2)

    app.logger.info('Creating Average liter: %s totalKm: %s, average: %s', liters, totalKm, avg_calc)

    return avg_calc