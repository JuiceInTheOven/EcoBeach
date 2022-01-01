package com.example.androidproject.models

import com.google.gson.annotations.SerializedName
import java.io.Serializable

data class BeachModel(
    @SerializedName("countryCode"        ) var countryCode       : String?      = null,
    @SerializedName("locationName"       ) var locationName      : String?      = null,
    @SerializedName("geoPosition"        ) var geoPosition       : GeoPosition? = GeoPosition(),
    @SerializedName("date"               ) var date              : String?      = null,
    @SerializedName("land_squareMeters"  ) var landSquareMeters  : Int?         = null,
    @SerializedName("land_percentage"    ) var landPercentage    : Double?      = null,
    @SerializedName("water_squareMeters" ) var waterSquareMeters : Int?         = null,
    @SerializedName("water_percentage"   ) var waterPercentage   : Double?      = null,
    @SerializedName("_id"                ) var Id                : String?      = null,
    @SerializedName("name"               ) var name              : String?      = null
): Serializable{
    override fun toString(): String {
        return "$locationName#${geoPosition!!.lat}#${geoPosition!!.lon}#$countryCode#$date#" +
                "$landSquareMeters#$landPercentage#$waterSquareMeters#$waterPercentage#$Id#$name"
    }
}

data class GeoPosition (

    @SerializedName("lat" ) var lat : Double? = null,
    @SerializedName("lon" ) var lon : Double? = null

): Serializable{}