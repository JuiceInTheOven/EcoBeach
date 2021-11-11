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
        //TODO("Not yet implemented")
        rendowWindowText(marker, mWindow)
        return mWindow
    }

    override fun getInfoContents(marker: Marker?): View {
        //TODO("Not yet implemented")
        rendowWindowText(marker, mWindow)
        return mWindow
    }


    var mContext = context
    var mWindow = (context as Activity).layoutInflater.inflate(R.layout.infowindowlayout, null)

    private fun rendowWindowText(marker: Marker?, view: View){

        //val image = view.findViewById<ImageView>(R.id.imageView1)
        val tvTitle = view.findViewById<TextView>(R.id.textView1)
        val tvSnippet = view.findViewById<TextView>(R.id.textView2)

        tvTitle.text = marker!!.title
        tvSnippet.text = marker!!.snippet


    }
}