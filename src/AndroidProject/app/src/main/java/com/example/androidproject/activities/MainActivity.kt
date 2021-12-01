package com.example.androidproject.activities

import android.Manifest
import android.content.pm.PackageManager
import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import com.example.androidproject.R
import com.example.androidproject.databinding.ActivityMainBinding
import com.example.androidproject.models.Beach
import com.example.androidproject.models.CustomMarker
import com.google.android.gms.location.FusedLocationProviderClient
import com.google.android.gms.location.LocationServices
import com.google.android.gms.maps.CameraUpdateFactory
import com.google.android.gms.maps.GoogleMap
import com.google.android.gms.maps.OnMapReadyCallback
import com.google.android.gms.maps.SupportMapFragment
import com.google.android.gms.maps.model.*
import android.content.Intent

class MainActivity : AppCompatActivity(), OnMapReadyCallback {

    private lateinit var mMap: GoogleMap
    private lateinit var binding: ActivityMainBinding
    private val locationRequest = 1
    private lateinit var fusedLocationClient: FusedLocationProviderClient
    private lateinit var userLocation: LatLng
    private var green: Float = 157f

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        fusedLocationClient = LocationServices.getFusedLocationProviderClient(this)
        getLastKnownLocation()
    }

    /**
     * Manipulates the map once available.
     * This callback is triggered when the map is ready to be used.
     * This is where we can add markers or lines, add listeners or move the camera. In this case,
     * we just add a marker near Sydney, Australia.
     * If Google Play services is not installed on the device, the user will be prompted to install
     * it inside the SupportMapFragment. This method will only be triggered once the user has
     * installed Google Play services and returned to the app.
     */
    override fun onMapReady(googleMap: GoogleMap) {
        mMap = googleMap

        addBeachesToMap()
        mMap.setInfoWindowAdapter(CustomMarker(this))

        //move the camera to the user's location
        mMap.moveCamera(CameraUpdateFactory.newLatLngZoom(userLocation, 10f))

        mMap.setOnInfoWindowClickListener { marker ->
            if(marker.title != "You are here :)"){
                val intent = Intent(this, BeachActivity::class.java).apply {
                    val info = marker.snippet.split(',')

                    putExtra("name", info[0])
                    putExtra("lat", info[1])
                    putExtra("lng", info[2])
                    putExtra("change", info[3])
                }
                startActivity(intent)
            }
        }
    }

    private fun addBeachesToMap(){
        // Add a marker to the user's location
        mMap.addMarker(MarkerOptions().position(userLocation).title("You are here :)").snippet(",${userLocation.latitude},${userLocation.longitude},"))

        val beaches = mutableListOf<Beach>()
        beaches.add(Beach("Kerteminde Nordstrand", 55.4578631605276, 10.66580564769334, 0.0))
        beaches.add(Beach("Hasmark Strand", 55.559144842780235, 10.466831402854728, 0.0))
        beaches.add(Beach("Nordenhuse Strand", 55.37738690518388, 10.771233901499762, 0.0))

        beaches.forEach{ beach ->
            mMap.addMarker(MarkerOptions().position(LatLng(beach.Lat, beach.Lng)).title(beach.Name).icon(
                BitmapDescriptorFactory.defaultMarker(green)).snippet(beach.toString()))
        }
    }

    private fun getLastKnownLocation() {
        if (ActivityCompat.checkSelfPermission(
                this,
                Manifest.permission.ACCESS_FINE_LOCATION
            ) != PackageManager.PERMISSION_GRANTED &&
            ActivityCompat.checkSelfPermission(
                this,
                Manifest.permission.ACCESS_COARSE_LOCATION
            ) != PackageManager.PERMISSION_GRANTED
        ) {
            ActivityCompat.requestPermissions(
                this,
                arrayOf(
                    Manifest.permission.ACCESS_FINE_LOCATION,
                    Manifest.permission.ACCESS_COARSE_LOCATION
                ), locationRequest
            )
            return
        }

        fusedLocationClient.lastLocation
            .addOnSuccessListener {location ->
                if (location != null) {
                    userLocation = LatLng(location.latitude, location.longitude)

                    // Obtain the SupportMapFragment and get notified when the map is ready to be used.
                    val mapFragment = supportFragmentManager.findFragmentById(R.id.map) as SupportMapFragment
                    mapFragment.getMapAsync(this)
                    }
            }
    }

    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<String>,
                                            grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        when (requestCode) {
            locationRequest -> {
                if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    if ((ContextCompat.checkSelfPermission(
                            this@MainActivity,
                            Manifest.permission.ACCESS_FINE_LOCATION
                        ) === PackageManager.PERMISSION_GRANTED)) {
                        Toast.makeText(this, "Permission Granted", Toast.LENGTH_SHORT).show()
                    }
                } else {
                    Toast.makeText(this, "Permission Denied", Toast.LENGTH_SHORT).show()
                }
                return
            }
        }
    }
}