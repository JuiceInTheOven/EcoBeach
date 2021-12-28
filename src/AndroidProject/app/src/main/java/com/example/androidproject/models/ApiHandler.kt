package com.example.androidproject.models

import com.android.volley.Request
import com.android.volley.Response
import com.android.volley.toolbox.JsonObjectRequest
import com.fasterxml.jackson.module.kotlin.jacksonObjectMapper
import com.fasterxml.jackson.module.kotlin.readValue

class ApiHandler{
    val url = "http://numbersapi.com/random/year?json"

    fun getDatas() : List<Beach>{
        val mapper = jacksonObjectMapper()

        //beaches.add(Beach("Kerteminde Nordstrand", 55.4578631605276, 10.66580564769334, 0.0))
        //beaches.add(Beach("Hasmark Strand", 55.559144842780235, 10.466831402854728, 0.0))

        //val json = getJson()

        val json = """[ {
                      "name" : "Kerteminde Nordstrand",
                      "lat" : "55.4578631605276",
                      "lng" : "10.66580564769334"
                    }, {
                      "name" : "Hasmark Strand",
                      "lat" : "55.559144842780235",
                      "lng" : "10.466831402854728"
                    } ]"""

        val beaches: List<Beach> = mapper.readValue(json)

        return beaches
    }

    private fun getJson() : String{
        var json : String = ""

        val jsonObjectRequest = JsonObjectRequest(
            Request.Method.GET, url, null,
            { response ->
                //textView.text = "Response: %s".format(response.toString())
                json = response.toString()
            },
            { _ -> //error
                // TODO: Handle error
                json = ""
            }
        )

        return json
    }
}