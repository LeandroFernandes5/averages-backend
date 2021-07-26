from app import app
from app.models import Supply, CarAverage
import datetime


"""
    Calculate average between 2 supplies, only used upon POST supply
"""
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


"""
    Function to calculate or re-calculate monthly average
"""
def monthlyAverageCalculation(supDate, carId):

    result = {}
    
    totalKm = Supply.get_total_km(supDate, carId)

    result['totalKm'] = totalKm

    aux = Supply.get_monthly_sup_range(supDate, carId)
    
    liters = Supply.get_liters_bt_sups(carId, aux)

    result['liters'] = liters

    monthlyAvg = Supply.calc_average(liters, totalKm)

    result['monthlyAvg'] = monthlyAvg

    CarAverage.create_or_update_car_average(supDate, carId, result)

    return result



