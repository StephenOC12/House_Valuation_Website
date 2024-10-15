from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
import mysql.connector

views = Blueprint('views',__name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/singleplayer')
@login_required
def showHouseInfo():
    db = mysql.connector.connect(
        host="77.68.35.85",
        user="y13stephen",
        password="d#5G1vz90",
        database="y13stephen"
    )

    global UsernamePython
    UsernamePython = current_user.UsernamePython


    cursorObjectHouse = db.cursor()

    questionNumberUsers = f"SELECT question_number FROM NEA_Users_Table WHERE username = '{UsernamePython}' "
    cursorObjectHouse.execute(questionNumberUsers)
    questionNumber = cursorObjectHouse.fetchone()[0]

    pythonTestHouse = f"SELECT * FROM kc_house_data_csv_zip WHERE id = '{questionNumber}'"
    cursorObjectHouse.execute(pythonTestHouse)
    resultHouse = cursorObjectHouse.fetchone()


    questionCounter = f"SELECT question_counter_mysql FROM NEA_Users_Table WHERE username = '{UsernamePython}' "
    cursorObjectHouse.execute(questionCounter)
    questionNumberTest = cursorObjectHouse.fetchone()[0]

    if int(questionNumberTest) %2 == 0:
        incrementQuestion = f"UPDATE NEA_Users_Table SET question_number = '{questionNumber+1}' WHERE username = '{UsernamePython}' "
        cursorObjectHouse.execute(incrementQuestion)
        incrementQuestionCounter = f"UPDATE NEA_Users_Table SET question_counter_mysql = '{questionNumberTest+1}' WHERE username = '{UsernamePython}' "
        cursorObjectHouse.execute(incrementQuestionCounter)
    else:
        incrementQuestionCounter = f"UPDATE NEA_Users_Table SET question_counter_mysql = '{questionNumberTest+1}' WHERE username = '{UsernamePython}' "
        cursorObjectHouse.execute(incrementQuestionCounter)


    secondHouse = getSecondHouseInfo(db, UsernamePython, questionNumber)



    db.commit()

    db.close()

    return render_template("singleplayer.html", user=current_user, resultHouse=resultHouse, secondHouse=secondHouse)

def getSecondHouseInfo(db, UsernamePython, questionNumber):
    cursorObjectHouse = db.cursor()

    # Get the second house information using a different query
    secondQuestionNumber = questionNumber + 1
    secondHouseQuery = f"SELECT * FROM kc_house_data_csv_zip WHERE id = '{secondQuestionNumber}'"
    cursorObjectHouse.execute(secondHouseQuery)
    secondHouse = cursorObjectHouse.fetchone()

    return secondHouse


@views.route('/profile')
@login_required
def profile():
    from .models import User

    return render_template("profile.html", user = current_user)

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split


@views.route('/valuation', methods=['GET', 'POST'])
@login_required
def valuation():
    if request.method == 'POST':
        usernameInput = request.form.get('usernameInput')
        addressInput = request.form.get('addressInput')
        bedroomInput = request.form.get('bedroomInput')
        bathroomInput = request.form.get('bathroomInput')
        sqftLivingInput = request.form.get('sqftLivingInput')
        sqftLotInput = request.form.get('sqftLotInput')
        floorInput = request.form.get('floorInput')
        waterfrontInput = request.form.get('waterfrontInput')
        viewInput = request.form.get('viewInput')
        conditionInput = request.form.get('conditionInput')
        gradeInput = request.form.get('gradeInput')
        sqftAboveInput = request.form.get('sqftAboveInput')
        sqftBasementInput = request.form.get('sqftBasementInput')
        yrBuiltInput = request.form.get('yrBuiltInput')
        yrRenovatedInput = request.form.get('yrRenovatedInput')
        zipcodeInput = request.form.get('zipcodeInput')
        latInput = request.form.get('latInput')
        longInput = request.form.get('longInput')
        sqftLiving15Input = request.form.get('sqftLiving15Input')
        sqftLot15Input = request.form.get('sqftLot15Input')

        #The part above retrieves all the data that was inputted from the HTML form to be used in the linear regression

        db = mysql.connector.connect(
            host="77.68.35.85",
            user="y13stephen",
            password="d#5G1vz90",
            database="y13stephen"
        )

        cursorObject = db.cursor()
        cursorObject.execute("SELECT * FROM kc_house_data_csv_zip")
        result = cursorObject.fetchall()

        houses = np.zeros((len(result), len(result[0])))

        for i in range(len(result)):
            for j in range(len(result[0])):
                if j == 1:
                    houses[i][j] = float(result[i][j][:8])
                else:
                    houses[i][j] = float(result[i][j])

        # The part above takes the data from the dataset about the houses and puts it in a more useful form
        # This is in part due to the fact that data given from strings vs csv files are outputted as varchar
        # with the format I have saved it in, but this for loop also creates a new list that allows me to separate
        # the prices of the houses which I can use as the dependent variable in the linear regression and in the other 2d
        # array I will have a list of the rest of the information about the houses where they are separated in the lines below.

        houseinfo = houses[:, 3:21]
        houseprices = houses[:, 2]

        kc_house_info = pd.DataFrame(houses,
                                     columns=["id", "date", "price", "bedrooms", "bathrooms", "sqft_living", "sqft_lot",
                                              "floors", "waterfront", "view", "condition", "grade", "sqft_above",
                                              "sqft_basement", "yr_built", "yr_renovated", "zipcode", "lat", "long",
                                              "sqft_living15", "sqft_lot15"])
        mean_by_bedrooms = kc_house_info.groupby("bedrooms").mean()
        # print(mean_by_bedrooms["price"])

        # This part does not necessarily affect the user's experience of the website but was key in understanding my
        # dataset better. I used this dataframe to show me the average prices of houses by number of bedrooms, so I
        # could determine if the values I received in the lasso regression were outliers or if it fit my data correctly.

        # listTemp = list(result)

        # array = np.array(result)
        # newarray = array[0:,2]

        # def functionTest(x):
        # x = list(x)
        # x.pop(1)
        # return x

        # I decided to change the element above to using the approach with the for loop, as a way of separating the
        # prices of the houses and the rest of the information. I left this to illustrate my design process and
        # left it in case I wanted to revert to my original approach.

        # new = list(map(functionTest,listTemp))
        # newtwo = list(map(functionTest,new))

        # print(newarray)
        # newone = np.array(newtwo)
        # print(newone)

        # In this part of the code I am now moving into the section of using linear regression to predict the value of
        # the end user's house. I have decided to split my data into a train test split to see how well my algorithm
        # performs. I will score this model afterwards to determine how closely the datapoints are correlated.

        X_train, X_test, y_train, y_test = train_test_split(houseinfo, houseprices, test_size=0.2, random_state=42)

        # print(X_train.shape)
        # print(X_test.shape)

        model = LinearRegression()
        model.fit(X_train, y_train)

        # print(model.score(X_test, y_test))

        # I hashed this part out of the program because it is not beneficial to the end user but allowed me to see the
        # performance of the linear regression algorithm. It returned a r^2 score of 0.67 which is relatively high
        # considering that my dataset has ~21,000 records which suggests that there is a high correlation between
        # the independent variables that I have selected to investigate and the dependent variable of the price.

        prediction = model.predict(X_test)

        # Lasso regression is another regression technique which will allow me to determine a relationship between
        # these variables. Lasso regression works by separating out each independent variable and determines a number
        # that the dependent variable will change by if you increment each independent variable by one. For example,
        # in my project I will determine how increasing the amount of bedrooms in a house by 1 will affect the price.

        lasso = Lasso(alpha=0.1)
        lasso.fit(X_train, y_train)

        kc_lasso_info = pd.DataFrame({
            "feature": ["bedrooms", "bathrooms", "sqft_living", "sqft_lot", "floors", "waterfront", "view", "condition",
                        "grade", "sqft_above", "sqft_basement", "yr_built", "yr_renovated", "zipcode", "lat", "long",
                        "sqft_living15", "sqft_lot15"],
            "amount": lasso.coef_
        })
        kc_lasso_info = kc_lasso_info.sort_values("amount", ascending=False)

        # I used this dataframe to represent the values that are calculated in the lasso regression. This will display
        # each independent variable (the 'feature' list) alongside the respective changes to the price they make.

        test_score = lasso.score(X_test, y_test)

        # print(kc_lasso_info)

        cursorObject = db.cursor()
        cursorObject.execute("DELETE FROM kc_house_data_csv_zip WHERE bedrooms = 33")
        db.commit()

        # predictionArray = np.array([bedroomInput, bathroomInput, sqftLivingInput, sqftLotInput, floorInput, waterfrontInput, viewInput, conditionInput, gradeInput, sqftAboveInput, sqftBasementInput, yrBuiltInput, yrRenovatedInput, zipcodeInput, latInput, longInput, sqftLiving15Input, sqftLot15Input])

        # predictionPrice = model.predict(predictionArray)
        # print(predictionPrice)

        user_input = pd.DataFrame([[bedroomInput, bathroomInput, sqftLivingInput, sqftLotInput, floorInput,
                                    waterfrontInput, viewInput, conditionInput, gradeInput, sqftAboveInput,
                                    sqftBasementInput, yrBuiltInput, yrRenovatedInput, zipcodeInput, latInput,
                                    longInput, sqftLiving15Input, sqftLot15Input]],
                                  columns=["bedrooms", "bathrooms", "sqft_living", "sqft_lot", "floors", "waterfront",
                                           "view", "condition", "grade", "sqft_above", "sqft_basement", "yr_built",
                                           "yr_renovated", "zipcode", "lat", "long", "sqft_living15", "sqft_lot15"])
        predictionPrice = model.predict(user_input)
        flash("the original price is:" + str(float(predictionPrice)), category="success")

        # print(predictionPrice)
        totalPrice = predictionPrice

        firstcursorObject = db.cursor()

        UserIDQuery = "SELECT UserID FROM NEA_Users_Table WHERE Username = %s"
        userValues = (usernameInput,)
        firstcursorObject.execute(UserIDQuery, userValues)

        UserID = firstcursorObject.fetchall()

        cursorObject = db.cursor()
        # print(predictionPrice)

        houseQuery = "INSERT INTO NEA_Houses_Table(UserID,Price,Address,ZIPCode,Bedrooms,Bathrooms,Sqft_Living,Sqft_Lot,Floors,Waterfront,View,House_Condition,Grade,Sqft_Above,Sqft_Basement,Yr_Built,Yr_Renovated,Latitude,Longitude,Sqft_Living15,Sqft_Lot15) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"
        val = (f"{UserID[0][0]}", f"{float(predictionPrice)}", f"{addressInput}", f"{zipcodeInput}", f"{bedroomInput}",
               f"{bathroomInput}", f"{sqftLivingInput}", f"{sqftLotInput}", f"{floorInput}", f"{waterfrontInput}",
               f"{viewInput}", f"{conditionInput}", f"{gradeInput}", f"{sqftAboveInput}", f"{sqftBasementInput}",
               f"{yrBuiltInput}", f"{yrRenovatedInput}", f"{latInput}", f"{longInput}", f"{sqftLiving15Input}",
               f"{sqftLot15Input}")
        cursorObject.execute(houseQuery, val)

        # print(UserID)

        db.commit()

        updateInput = request.form.get('updateInput')

        featuresSelected = updateInput.split(",")


        for feature in featuresSelected:
            featurePrice = kc_lasso_info.loc[kc_lasso_info['feature'] == feature, 'amount'].values[0]
            totalPrice += featurePrice

        # print("Features selected: ", featuresSelected)
        flash("The final price is: " + str(float(totalPrice)), category="success")

        countBathrooms = featuresSelected.count("bathrooms")
        countBedrooms = featuresSelected.count("bedrooms")
        countSqftLiving = featuresSelected.count("sqft_living")
        countSqftLot = featuresSelected.count("sqft_lot")
        countFloors = featuresSelected.count("floors")
        countWaterfront = featuresSelected.count("waterfront")
        countView = featuresSelected.count("view")
        countCondition = featuresSelected.count("condition")
        countGrade = featuresSelected.count("grade")
        countSqftAbove = featuresSelected.count("sqft_above")
        countSqftBasement = featuresSelected.count("sqft_basement")
        countYrBuilt = featuresSelected.count("yr_built")
        countYrRenovated = featuresSelected.count("yr_renovated")
        countZipcode = featuresSelected.count("zipcode")
        countLat = featuresSelected.count("lat")
        countLong = featuresSelected.count("long")
        countSqftLiving15 = featuresSelected.count("sqft_living15")
        countSqftLot15 = featuresSelected.count("sqft_lot15")



        HouseIDQuery = "SELECT HouseID FROM NEA_Houses_Table WHERE Address = %s"
        houseValues = (addressInput,)
        cursorObject.execute(HouseIDQuery,houseValues)

        HouseID = cursorObject.fetchall()

        db.commit()

        newcursorObject = db.cursor()

        totalBedrooms = float(bedroomInput) + float(countBedrooms)
        totalBathrooms = float(bathroomInput) + float(countBathrooms)
        totalSqftLiving = float(sqftLivingInput) + float(countSqftLiving)
        totalSqftLot = float(sqftLotInput) + float(countSqftLot)
        totalFloor = float(floorInput) + float(countFloors)
        totalWaterfront = float(waterfrontInput) + float(countWaterfront)
        totalView = float(viewInput) + float(countView)
        totalCondition = float(conditionInput) + float(countCondition)
        totalGrade = float(gradeInput) + float(countGrade)
        totalSqftAbove = float(sqftAboveInput) + float(countSqftAbove)
        totalSqftBasement = float(sqftBasementInput) + float(countSqftBasement)
        totalYrBuilt = float(yrBuiltInput) + float(countYrBuilt)
        totalYrRenovated = float(yrRenovatedInput) + float(countYrRenovated)
        totalLat = float(latInput) + float(countLat)
        totalLong = float(longInput) + float(countLong)
        totalZipcode = float(zipcodeInput) + float(countZipcode)
        totalSqftLiving15 = float(sqftLiving15Input) + float(countSqftLiving15)
        totalSqftLot15 = float(sqftLot15Input) + float(countSqftLot15)

        # print(HouseID)

        HouseQueryUpdate = "INSERT INTO NEA_Updates_Table(HouseID,New_Price,New_Bedrooms,New_Bathrooms,New_Sqft_Living,New_Sqft_Lot,New_Floors,New_Waterfront,New_View,New_Condition,New_Grade,New_Sqft_Above,New_Sqft_Basement,New_Yr_Built,New_Yr_Renovated,New_Zipcode,New_Lat,New_Long,New_Sqft_Living15,New_Sqft_Lot15) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (
        f"{HouseID}", f"{float(totalPrice)}", f"{totalBedrooms}", f"{totalBathrooms}",
        f"{totalSqftLiving}", f"{totalSqftLot}", f"{totalFloor}",
        f"{totalWaterfront}", f"{totalView}", f"{totalCondition}",
        f"{totalGrade}", f"{totalSqftAbove}", f"{totalSqftBasement}",
        f"{totalYrBuilt}", f"{totalYrRenovated}", f"{totalLat}",
        f"{totalLong}", f"{totalZipcode}", f"{totalSqftLiving15}",
        f"{totalSqftLot15}")
        newcursorObject.execute(HouseQueryUpdate, values)

        db.commit()

        db.close()

    return render_template("houseprediction.html", user=current_user)