package com.example.androidproject.models

import android.app.Activity
import android.content.Context
import android.view.View
import android.widget.TextView
import com.example.androidproject.R
import com.google.android.gms.maps.GoogleMap
import com.google.android.gms.maps.model.Marker

class CustomMarker (context: Context) : GoogleMap.InfoWindowAdapter {
    private var _context: Context = context


    override fun getInfoWindow(marker: Marker?): View? {
        return null
    }

    override fun getInfoContents(marker: Marker?): View {
        setWindowTexts(marker, mWindow)
        return mWindow
    }

    private var mWindow = (context as Activity).layoutInflater.inflate(R.layout.infowindowlayout, null)

    private fun setWindowTexts(marker: Marker?, view: View){
        val title = view.findViewById<TextView>(R.id.info_title)
        val lat = view.findViewById<TextView>(R.id.info_lat)
        val lng = view.findViewById<TextView>(R.id.info_lng)

        val latLng = marker!!.snippet.split(',')

        val latRounded = "%.2f".format(latLng[1].toDouble())
        val lngRounded = "%.2f".format(latLng[2].toDouble())

        title.text = marker.title

        lat.text = _context.resources.getString(R.string.lat_text, latRounded)
        lng.text = _context.resources.getString(R.string.lng_text, lngRounded)
    }
}