package com.example.androidproject.models

import android.app.Activity
import android.content.Context
import android.view.View
import android.widget.ImageView
import android.widget.TextView
import com.example.androidproject.R
import com.google.android.gms.maps.GoogleMap
import com.google.android.gms.maps.model.Marker

class CustomMarker (context: Context) : GoogleMap.InfoWindowAdapter {
    override fun getInfoWindow(marker: Marker?): View {
        setWindowTexts(marker, mWindow)
        return mWindow
    }

    override fun getInfoContents(marker: Marker?): View {
        setWindowTexts(marker, mWindow)
        return mWindow
    }

    var mContext = context
    var mWindow = (context as Activity).layoutInflater.inflate(R.layout.infowindowlayout, null)

    private fun setWindowTexts(marker: Marker?, view: View){
        //val image = view.findViewById<ImageView>(R.id.info_image)
        val title = view.findViewById<TextView>(R.id.info_title)
        val lat = view.findViewById<TextView>(R.id.info_lat)
        val lng = view.findViewById<TextView>(R.id.info_lng)

        var latLng = marker!!.snippet.split(',')

        title.text = marker!!.title
        lat.text = "Lat: ${latLng[1]}" //marker!!.snippet
        lng.text = "Lng: ${latLng[2]}"
    }
}