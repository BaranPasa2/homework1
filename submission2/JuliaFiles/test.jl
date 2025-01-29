using Pkg
using CSV, DataFrames

Pkg.add("CSV")

# Reading the files

using DataFrames; altContractData = CSV.read("data/input/CPSC_Contract_Info_2015_01.csv", DataFrame; missingstring="")
using DataFrames; altEnrollmentData = CSV.read("data/input/CPSC_Enrollment_Info_2015_01.csv", DataFrame; missingstring="")
using DataFrames; altServAreaData = CSV.read("data/input/MA_Cnty_SA_2015_01.csv", DataFrame; missingstring="")

# Checking to see the column header names:
foreach(println, names(altContractData))
foreach(println, names(altEnrollmentData))
#foreach(println, names(altServAreaData))

# merging the datasets:
innerjoin(altContractData, altEnrollmentData, on=:["Contract ID" => "Contract Number", :"Plan ID"], matchmissing=:notequal)