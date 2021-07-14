from app import app, db
from app.models import Supply, CarAverage
import datetime
from sqlalchemy import func

def averageCalculation(result):

    avg_calc = 0
    fullTank = result.get('fullTank')

    if fullTank:

        carId = result.get('carId')
        supplyDate = result.get('supplyDate')
        
        sups = Supply.query.filter(Supply.carId == carId).order_by(Supply.id.desc())

        supsfullTank = sups.filter(Supply.fullTank == True)

        if supsfullTank.count() >= 1 and supplyDate.date() == datetime.date.today():
            
            totalKm = result.get('totalKm')
            liters = result.get('liters')

            for supply in sups:
                if supply.fullTank:

                    totalKm = totalKm - supply.totalKm
                    break
                else:
                    liters = liters + supply.liters

            avg_calc = round((100 * liters) / totalKm, 2)

            app.logger.info('Creating Average liter: %s totalKm: %s, average: %s', liters, totalKm, avg_calc)

        
        currentMonth = supplyDate.date().replace(day=1)

        if supsfullTank.filter(Supply.supplyDate >=  currentMonth).count() >= 1:

            allSupsCurrentMonth = sups.filter(Supply.supplyDate >= currentMonth).order_by(Supply.id.asc())

            max_km = db.session.query(db.func.max(Supply.average)).filter(Supply.supplyDate >= currentMonth).filter(Supply.carId == carId).filter(Supply.fullTank == True).scalar()
            min_km = db.session.query(db.func.min(Supply.average)).filter(Supply.supplyDate >= currentMonth).filter(Supply.carId == carId).filter(Supply.fullTank == True).scalar()

            totalKm = max_km - min_km

            for sup in reversed(allSupsCurrentMonth):
                if sup.id == allSupsCurrentMonth.first().id:
                    break
                else:
                    liters = liters + sup.liters

            monthlyAvg = round((100 * liters) / totalKm, 2)

            exitsAverage = db.session.query(CarAverage).filter(CarAverage.year == currentMonth.year).filter(CarAverage.month == currentMonth.year).filter(CarAverage.carId == carId).first()

            # if exitsAverage:
            #     exitsAverage.

            pass

    return avg_calc