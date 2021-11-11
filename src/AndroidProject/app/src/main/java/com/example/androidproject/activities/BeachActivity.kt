package com.example.androidproject.activities

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import com.example.androidproject.R
import com.example.androidproject.models.Beach

class BeachActivity : AppCompatActivity() {
    private lateinit var beach: Beach

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
        this.findViewById<TextView>(R.id.beach_lat).text = "Lat: " + beach.Lat.toString()
        this.findViewById<TextView>(R.id.beach_lng).text = "Lng: " + beach.Lng.toString()

        val closeButton = this.findViewById<Button>(R.id.close_beach_btn).setOnClickListener(){
            this.finish()
        }
    }
}