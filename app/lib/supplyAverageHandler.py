from app import app, db
from app.models import Supply
from app.lib.businessLogic import *
from sqlalchemy import func

"""
    Function to deal with supply outcomes of DEL a supply
"""
def delSupply(supply):

    carId = supply.carId
    supDate = supply.supplyDate

    supRange = Supply.get_sup_range(supDate, carId)

    """
        Update next Supply average
    """  
    if supRange is not None:
        
        if not supRange[-1].isSupplyPast:
            
            totalKm = supRange[-1].totalKm - supRange[0].totalKm

            liters = db.session.query(func.sum(Supply.liters)).filter(Supply.carId == carId, Supply.totalKm.between(supRange[1].totalKm, supRange[-1].totalKm)).scalar() 

            avg = Supply.calc_average(liters, totalKm)

            nextSup = Supply.get_next_sup(supDate, carId)

            nextSup.average = avg

            db.session.commit()

            app.logger.info('Re-calc of average for Car: %s totalKm: %s, liters: %s, average: %s',carId, totalKm, liters, avg)

        """
            Delete or re-calc monthly average
        """
        monthlySups = Supply.get_monthly_sups(supDate, carId)

        if monthlySups.count() > 1:

            monthlyAverageCalculation(supDate, carId)

            db.session.commit()

        elif monthlySups.count() == 1:
            
            CarAverage.get_delete_car_average(supDate, carId)
            
            db.session.commit()


"""
    Deal with possible outcomes of POST supply
"""
def postSupply(supply):

        if supply.fullTank:

            sups = Supply.get_monthly_sups(supply.supplyDate, supply.carId)
        
            if sups.count() > 1:

                monthlyAverageCalculation(supply.supplyDate, supply.carId)

                db.session.commit()