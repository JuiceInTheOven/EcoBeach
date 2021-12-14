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
import com.google.android.gms.maps.CameraUpdateFactory
import com.google.android.gms.maps.GoogleMap
import com.google.android.gms.maps.OnMapReadyCallback
import com.google.android.gms.maps.SupportMapFragment
import com.google.android.gms.maps.model.*
import android.content.Intent
import android.location.LocationManager
import android.content.DialogInterface
import android.provider.Settings
import android.app.AlertDialog.Builder
import android.content.Context
import android.net.ConnectivityManager
import android.net.NetworkCapabilities
import android.os.Build
import com.example.androidproject.models.ApiHandler
import com.google.android.gms.location.*

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

        checkGPS()
        checkInternet(this)
    }

    private fun checkInternet(context: Context){
        if(checkForInternet(context)){
            //Toast.makeText(this, "Internet is Enabled in your device", Toast.LENGTH_SHORT).show()
        }
        else{
            val builder = Builder(this)
            builder
                .setTitle("There's no Internet connection")
                .setMessage("For a better experience, turn on Internet connection. If you pick OK, the application will be closed. " +
                        "Please restart the app after you have turned on the internet.")
                .setPositiveButton("OK") { _, _ -> finish() }
                .setNegativeButton("No thanks") { _, _ ->  }
            // Create the AlertDialog object and return it
            builder.create().show()
        }
    }

    private fun checkForInternet(context: Context): Boolean {

        // register activity with the connectivity manager service
        val connectivityManager = context.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager


        // if the android version is equal to M
        // or greater we need to use the
        // NetworkCapabilities to check what type of
        // network has the internet connection
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {

            // Returns a Network object corresponding to
            // the currently active default data network.
            val network = connectivityManager.activeNetwork ?: return false

            // Representation of the capabilities of an active network.
            val activeNetwork = connectivityManager.getNetworkCapabilities(network) ?: return false

            return when {
                // Indicates this network uses a Wi-Fi transport,
                // or WiFi has network connectivity
                activeNetwork.hasTransport(NetworkCapabilities.TRANSPORT_WIFI) -> true

                // Indicates this network uses a Cellular transport. or
                // Cellular has network connectivity
                activeNetwork.hasTransport(NetworkCapabilities.TRANSPORT_CELLULAR) -> true

                // else return false
                else -> false
            }
        } else {
            // if the android version is below M
            @Suppress("DEPRECATION") val networkInfo =
                connectivityManager.activeNetworkInfo ?: return false
            @Suppress("DEPRECATION")
            return networkInfo.isConnected
        }
    }

    private fun checkGPS(){
        val mLocationManager = getSystemService(Context.LOCATION_SERVICE) as LocationManager
        // Checking GPS is enabled
        val isGPSEnabled = mLocationManager.isProviderEnabled(LocationManager.GPS_PROVIDER)
        if(isGPSEnabled){
            //Toast.makeText(this, "GPS is Enabled in your device", Toast.LENGTH_SHORT).show()
            fusedLocationClient = LocationServices.getFusedLocationProviderClient(this)
            getLastKnownLocation()
        }
        else{

            //Toast.makeText(this, "GPS is not Enabled in your devide", Toast.LENGTH_SHORT).show()
            val builder = Builder(this)
            builder
                .setTitle("GPS is not enabled")
                .setMessage("For a better experience, turn on device location")
                .setPositiveButton("OK") { _, _ ->
                    val intent = Intent(Settings.ACTION_LOCATION_SOURCE_SETTINGS)
                    startActivity(intent)
                    finish()
                }
                .setNegativeButton("No thanks") { _, _ -> finish() }
            // Create the AlertDialog object and return it
            builder.create().show()
        }
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

    private fun addBeachesToMap() {
        // Add a marker to the user's location
        mMap.addMarker(
            MarkerOptions().position(userLocation).title("You are here :)")
                .snippet(",${userLocation.latitude},${userLocation.longitude},")
        )

//        val beaches = mutableListOf<Beach>()
//        beaches.add(Beach("Kerteminde Nordstrand", 55.4578631605276, 10.66580564769334, 0.0))
//        beaches.add(Beach("Hasmark Strand", 55.559144842780235, 10.466831402854728, 0.0))
//        beaches.add(Beach("Nordenhuse Strand", 55.37738690518388, 10.771233901499762, 0.0))

        val apiHandler = ApiHandler()
        val beaches = apiHandler.getDatas()

        beaches.forEach { beach ->
            mMap.addMarker(
                MarkerOptions().position(LatLng(beach.Lat, beach.Lng)).title(beach.Name).icon(
                    BitmapDescriptorFactory.defaultMarker(green)
                ).snippet(beach.toString())
            )
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
                        startActivity(this.intent)
                    }
                } else {
                    Toast.makeText(this, "Permission Denied", Toast.LENGTH_SHORT).show()
                    finish()
                }
                return
            }
        }
    }
}