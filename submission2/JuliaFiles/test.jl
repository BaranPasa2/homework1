using Pkg
using CSV, DataFrames

Pkg.add("CSV")

# Reading the files
contractData = CSV.read("data/input/CPSC_Contract_Info_2015_01.csv", DataFrame)
enrollmentData = CSV.read("data/input/CPSC_Enrollment_Info_2015_01.csv", DataFrame)
serviceAreaData = CSV.read("data/input/MA_Cnty_SA_2015_01.csv", DataFrame)


# Create a new DataFrame with only complete cases. 
contractDataClean = contractData[completecases(contractData), :]
enrollmentDataClean = enrollmentData[completecases(enrollmentData), :]
serviceAreaDataClean = serviceAreaData[completecases(serviceAreaData),:]

# Now printing to check how many rows have been removed:
println("CONTRACT DATA:")
println("Column names: ", names(contractDataClean))
println("Number of rows: ", nrow(contractData))
println("Number of cleaned rows: ", nrow(contractDataClean))
println("Number of columns: ", ncol(contractData))
println("number of cleaned columns: ", ncol(contractDataClean))

println("ENROLLMENT DATA")
println("Column names: ", names(enrollmentDataClean))
println("Number of rows: ", nrow(enrollmentData))
println("Number of cleaned rows: ", nrow(enrollmentDataClean))
println("Number of columns: ", ncol(enrollmentData))
println("number of cleaned columns: ", ncol(enrollmentDataClean))

println("SERVICE AREA DATA")
println("Column names: ", names(serviceAreaDataClean))
println("Number of rows: ", nrow(serviceAreaData))
println("Number of cleaned rows: ", nrow(serviceAreaDataClean))
println("Number of columns: ", ncol(serviceAreaData))
println("number of cleaned columns: ", ncol(serviceAreaDataClean))
