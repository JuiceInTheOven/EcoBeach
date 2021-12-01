package com.example.androidproject.activities

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import com.example.androidproject.R
import com.example.androidproject.models.Beach
import com.google.android.gms.maps.CameraUpdateFactory
import com.google.android.gms.maps.GoogleMap
import com.google.android.gms.maps.MapView
import com.google.android.gms.maps.OnMapReadyCallback
import com.google.android.gms.maps.model.LatLng


class BeachActivity : AppCompatActivity(), OnMapReadyCallback {
    private lateinit var beach: Beach
    private lateinit var mapView: MapView
    private lateinit var gmap: GoogleMap
    private val MAP_VIEW_BUNDLE_KEY : String = "MapViewBundleKey"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_beach)

        beach = Beach(
            intent.extras?.get("name").toString(),
            intent.extras?.get("lat").toString().toDouble(),
            intent.extras?.get("lng").toString().toDouble(),
            intent.extras?.get("change").toString().toDouble()
        )

        this.findViewById<TextView>(R.id.beach_title).text = beach.Name
        val latRounded = "%.2f".format(beach.Lat).toDouble()
        val lngRounded = "%.2f".format(beach.Lng).toDouble()

        this.findViewById<TextView>(R.id.beach_lat).text = "Lat: " + latRounded.toString()
        this.findViewById<TextView>(R.id.beach_lng).text = "Lng: " + lngRounded.toString()

        val closeButton = this.findViewById<Button>(R.id.close_beach_btn).setOnClickListener(){
            this.finish()
        }

        var mapViewBundle: Bundle? = null
        if (savedInstanceState != null) {
            mapViewBundle = savedInstanceState.getBundle(MAP_VIEW_BUNDLE_KEY)
        }

        mapView = findViewById(R.id.mapView)
        mapView.onCreate(mapViewBundle)

        mapView.getMapAsync(this)
    }

    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState)
        var mapViewBundle = outState.getBundle(MAP_VIEW_BUNDLE_KEY)
        if (mapViewBundle == null) {
            mapViewBundle = Bundle()
            outState.putBundle(MAP_VIEW_BUNDLE_KEY, mapViewBundle)
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
        gmap = googleMap
        gmap.setMinZoomPreference(14f)
        gmap.mapType = GoogleMap.MAP_TYPE_SATELLITE
        val ny = LatLng(beach.Lat, beach.Lng)
        gmap.moveCamera(CameraUpdateFactory.newLatLng(ny))
    }
}