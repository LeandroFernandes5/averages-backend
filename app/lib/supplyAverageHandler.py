from app import app, db
from app.models import Supply
from app.lib.businessLogic import *
from sqlalchemy import extract

def delSupply(supply):

    carId = supply.carId
    supDate = supply.supplyDate

    supRange = Supply.get_sup_range(supDate, carId)
                
    if supRange is not None:
        
        monthlyAverageCalculation(supDate, carId)

        db.session.commit()

        if not supRange[-1].isSupplyPast:
            
            totalKm = supRange[-1].totalKm - supRange[0].totalKm

            liters = db.session.query(func.sum(Supply.liters)).filter(Supply.carId == carId, Supply.totalKm.between(supRange[1].totalKm, supRange[-1].totalKm)).scalar() 

            avg = Supply.calc_average(liters, totalKm)

            nextSup = Supply.get_next_sup(supDate, carId)

            nextSup.average = avg

            db.session.commit()

            app.logger.info('Re-calc of average for Car: %s totalKm: %s, liters: %s, average: %s',carId, totalKm, liters, avg)


def postSupply(supply):

        if supply.fullTank:
            
            carId = supply.carId
            supplyDate = supply.supplyDate

            sups = db.session.query(Supply).filter(Supply.carId == carId, extract('year', Supply.supplyDate) == supplyDate.year, extract('month', Supply.supplyDate) == supplyDate.month).order_by(Supply.id.desc())
        
            if sups.filter(Supply.fullTank == True).count() > 1:

                monthlyAverageCalculation(supplyDate, carId)

                db.session.commit()