from sqlalchemy.sql.expression import exists
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

        
    return avg_calc

        

def averageMonthlyCalculation(supply):

        if supply.fullTank:
            
            carId = supply.carId
            supplyDate = supply.supplyDate

            currentMonth = supplyDate.date().replace(day=1)

            sups = Supply.query.filter(Supply.carId == carId).filter(Supply.supplyDate >= currentMonth).order_by(Supply.id.desc())
        
            if sups.filter(Supply.fullTank == True).count() > 1:

                max_km = db.session.query(db.func.max(Supply.totalKm)).filter(Supply.supplyDate >= currentMonth).\
                    filter(Supply.carId == carId).filter(Supply.fullTank == True).scalar()
                
                min_km = db.session.query(db.func.min(Supply.totalKm)).filter(Supply.supplyDate >= currentMonth).\
                    filter(Supply.carId == carId).filter(Supply.fullTank == True).scalar()

                totalKm = max_km - min_km
                
                aux = db.session.query(Supply).filter(Supply.supplyDate >= currentMonth).\
                    filter(Supply.carId == carId).filter(Supply.fullTank == True).order_by(Supply.totalKm.asc())

                liters = db.session.query(func.sum(Supply.liters)).filter(Supply.supplyDate >= currentMonth).filter(Supply.carId == carId).\
                    filter(Supply.totalKm.between(aux[1].totalKm, aux[-1].totalKm)).scalar()

                print('liters')
                print(type(liters))
                print(liters)
                print('totalKm')
                print(type(totalKm))
                print(totalKm)
                monthlyAvg = round((100 * liters) / totalKm, 2)

                existsAverage = CarAverage.query.filter_by(year=currentMonth.year).filter_by(month=currentMonth.month).filter_by(carId = carId).first()
                
                if existsAverage:
                    
                    existsAverage.average = monthlyAvg
                    existsAverage.liters = liters
                    existsAverage.km = totalKm

                    db.session.commit()

                    app.logger.info('Updated Monthly Average with id: %s, liter: %s totalKm: %s, average: %s', existsAverage.id, liters, totalKm, monthlyAvg)

                else:
                    average = CarAverage(
                        liters = liters,
                        km = totalKm,
                        year = currentMonth.year,
                        month = currentMonth.month,
                        carId = carId,
                        average = monthlyAvg
                    )

                    db.session.add(average)
                    db.session.commit()

                    app.logger.info('Created Monthly Average with liter: %s totalKm: %s, average: %s',liters, totalKm, monthlyAvg)


def delAverage(supply):

    carId = supply.carId
    supDate = supply.supplyDate

    nextSups = db.session.query(Supply).filter(Supply.supplyDate >= supDate).\
                    filter(Supply.carId == carId).filter(Supply.fullTank == True).order_by(Supply.totalKm.asc())
                
    if nextSups is not None:

        nextSup = nextSups[1]

        if not nextSup.isSupplyPast:

            beforeSups = db.session.query(Supply).filter(Supply.supplyDate <= supDate).\
                            filter(Supply.carId == carId).filter(Supply.fullTank == True).order_by(Supply.totalKm.desc())

            beforeSup = beforeSups[1]

            totalKm = nextSup.totalKm - beforeSup.totalKm

            currentMonth = supDate.date().replace(day=1)    

            aux = db.session.query(Supply).filter(Supply.supplyDate >= currentMonth).\
                            filter(Supply.carId == carId).filter(Supply.fullTank == True).order_by(Supply.totalKm.asc())

            liters = db.session.query(func.sum(Supply.liters)).filter(Supply.supplyDate >= currentMonth).filter(Supply.carId == carId).\
                            filter(Supply.id.between(aux[1].id, aux[-1].id)).scalar()


            avg = round((100 * liters) / totalKm, 2)

            nextSup.average = avg

            db.session.commit()

            app.logger.info('Re-calc of average for Car: %s totalKm: %s, liters: %s, average: %s',carId, totalKm, liters, avg)

            #call re-calc month average
