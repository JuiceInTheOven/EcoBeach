package com.example.androidproject.activities

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import com.example.androidproject.R
import com.example.androidproject.models.BeachModel
import com.google.android.gms.maps.CameraUpdateFactory
import com.google.android.gms.maps.GoogleMap
import com.google.android.gms.maps.MapView
import com.google.android.gms.maps.OnMapReadyCallback
import com.google.android.gms.maps.model.LatLng

class BeachActivity : AppCompatActivity(), OnMapReadyCallback {
    private lateinit var beach: BeachModel
    private lateinit var mapView: MapView
    private lateinit var gMap: GoogleMap
    private val mapViewBundleKey : String = "MapViewBundleKey"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_beach)

        beach = intent.extras?.getSerializable("beach") as BeachModel

        this.findViewById<TextView>(R.id.beach_title).text = beach.locationName
        val latRounded = "%.2f".format(beach.geoPosition!!.lat).toDouble()
        val lngRounded = "%.2f".format(beach.geoPosition!!.lon).toDouble()

        val landP = beach.landPercentage!!.times(100)
        val waterP = beach.waterPercentage!!.times(100)
        val landPercentageRounded = "%.2f".format(landP).toDouble()
        val waterPercentageRounded = "%.2f".format(waterP).toDouble()

        this.findViewById<TextView>(R.id.beach_lat).text = resources.getString(R.string.lat_text, latRounded.toString())
        this.findViewById<TextView>(R.id.beach_lng).text = resources.getString(R.string.lng_text, lngRounded.toString())
        this.findViewById<TextView>(R.id.date).text = resources.getString(R.string.date_text, beach.date)
        this.findViewById<TextView>(R.id.land).text = resources.getString(R.string.land_text, landPercentageRounded.toString())
        this.findViewById<TextView>(R.id.water).text = resources.getString(R.string.water_text, waterPercentageRounded.toString())

        this.findViewById<Button>(R.id.close_beach_btn).setOnClickListener{
            this.finish()
        }

        var mapViewBundle: Bundle? = null
        if (savedInstanceState != null) {
            mapViewBundle = savedInstanceState.getBundle(mapViewBundleKey)
        }

        mapView = findViewById(R.id.mapView)
        mapView.onCreate(mapViewBundle)

        mapView.getMapAsync(this)
    }

    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState)
        var mapViewBundle = outState.getBundle(mapViewBundleKey)
        if (mapViewBundle == null) {
            mapViewBundle = Bundle()
            outState.putBundle(mapViewBundleKey, mapViewBundle)
        }
        mapView.onSaveInstanceState(mapViewBundle)
    }

    override fun onResume() {
        super.onResume()
        mapView.onResume()
    }

    override fun onStart() {
        super.onStart()
        mapView.onStart()
    }

    override fun onStop() {
        super.onStop()
        mapView.onStop()
    }

    override fun onPause() {
        mapView.onPause()
        super.onPause()
    }

    override fun onDestroy() {
        mapView.onDestroy()
        super.onDestroy()
    }

    override fun onLowMemory() {
        super.onLowMemory()
        mapView.onLowMemory()
    }

    override fun onMapReady(googleMap: GoogleMap) {
        gMap = googleMap
        gMap.setMinZoomPreference(14f)
        gMap.mapType = GoogleMap.MAP_TYPE_SATELLITE
        val ny = LatLng(beach.geoPosition!!.lat!!.toDouble(), beach.geoPosition!!.lon!!.toDouble())
        gMap.moveCamera(CameraUpdateFactory.newLatLng(ny))
    }
}