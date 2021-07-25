from app import app, db
from app.models import Supply, CarAverage
import datetime
from sqlalchemy import func

def averageCalculation(supply):

    avg_calc = 0
    fullTank = supply.fullTank

    if fullTank:

        carId = supply.carId
        supplyDate = supply.supplyDate
        
        sups = Supply.query.filter(Supply.carId == carId).order_by(Supply.id.desc())

        supsfullTank = sups.filter(Supply.fullTank == True)

        if supsfullTank.count() >= 1 and supplyDate.date() == datetime.date.today():
            
            totalKm = supply.totalKm
            liters = supply.liters

            for supply in sups:
                if supply.fullTank:

                    totalKm = totalKm - supply.totalKm
                    break
                else:
                    liters = liters + supply.liters

            avg_calc = Supply.calc_average(liters, totalKm)

            app.logger.info('Creating Average liter: %s totalKm: %s, average: %s', liters, totalKm, avg_calc)

        
    return avg_calc

        
def monthlyAverage(carId, supDate):

    result = {}

    totalKm = Supply.get_total_km(supDate, carId)

    result['totalKm'] = totalKm
    
    aux = db.session.query(Supply).filter(Supply.supplyDate >= supDate, Supply.carId == carId, Supply.fullTank == True).order_by(Supply.totalKm.asc())

    liters = Supply.get_liters_bt_sups(supDate, carId, aux)

    result['liters'] = liters

    monthlyAvg = Supply.calc_average(liters, totalKm)

    result['monthlyAvg'] = monthlyAvg

    return result
    



def averageMonthlyCalculation(supply):

        if supply.fullTank:
            
            carId = supply.carId
            supplyDate = supply.supplyDate

            supDate = supplyDate.date().replace(day=1)

            sups = Supply.query.filter(Supply.carId == carId, Supply.supplyDate >= supDate).order_by(Supply.id.desc())
        
            if sups.filter(Supply.fullTank == True).count() > 1:

                result = monthlyAverage(carId, supDate)

                existsAverage = CarAverage.get_car_average(supDate, carId)
                
                if existsAverage:

                    existsAverage.update_car_average(result)
                    
                    db.session.commit()

                    app.logger.info('Updated Monthly Average with id: %s, liter: %s totalKm: %s, average: %s', existsAverage.id, result['liters'], result['totalKm'], result['monthlyAvg'])

                else:
                    
                    CarAverage.add_car_average(supDate, carId, result)

                    db.session.commit()

                    app.logger.info('Created Monthly Average with liter: %s totalKm: %s, average: %s', result['liters'], result['totalKm'], result['monthlyAvg'])


def delAverage(supply):

    carId = supply.carId
    supDate = supply.supplyDate

    nextSups = Supply.get_next_sups(supDate, carId)
                
    if nextSups is not None:

        if not nextSups[1].isSupplyPast:

            beforeSups = db.session.query(Supply).filter(Supply.supplyDate <= supDate, Supply.carId == carId, Supply.fullTank == True).order_by(Supply.totalKm.desc())

            beforeSup = beforeSups[1]

            totalKm = nextSups[1].totalKm - beforeSup.totalKm

            currentMonth = supDate.date().replace(day=1)    

            aux = Supply.get_aux_sups(currentMonth, carId)

            liters = Supply.get_liters_bt_sups(supDate, carId, aux)

            avg = Supply.calc_average(liters, totalKm)

            nextSups[1].average = avg

            db.session.commit()

            app.logger.info('Re-calc of average for Car: %s totalKm: %s, liters: %s, average: %s',carId, totalKm, liters, avg)

            #call re-calc month average
