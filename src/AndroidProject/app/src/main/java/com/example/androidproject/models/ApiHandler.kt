package com.example.androidproject.models

import android.content.Context
import com.example.androidproject.activities.MainActivity
import okhttp3.OkHttpClient
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.GET
import okhttp3.logging.HttpLoggingInterceptor

class ApiHandler (context: Context) {
    private var _context: Context = context
    private val url = "http://135.181.80.186:8085/"

    fun getBeachesOnMap(){
        val logging = HttpLoggingInterceptor()
        logging.level = HttpLoggingInterceptor.Level.BODY

        val client = OkHttpClient.Builder()
            .addInterceptor(logging)
            .build()

        val retrofit = Retrofit.Builder()
            .baseUrl(url)
            .addConverterFactory(GsonConverterFactory.create())
            .client(client)
            .build()

        val apiService: ApiEndpoints = retrofit.create(ApiEndpoints::class.java)

        var allBeaches : MutableList<BeachModel> = mutableListOf<BeachModel>()

        val call: Call<List<BeachModel>> = apiService.getBeaches()
        call.enqueue(object : Callback<List<BeachModel>> {
            override fun onResponse(call: Call<List<BeachModel>>, response: Response<List<BeachModel>>){
//                response.body()?.forEach { beach ->
//                    if((response.body() as List<BeachModel>).filter { it.locationName == beach.locationName}.count() == 1)
//                    {
//                        allBeaches.add(beach)
//                    }

//                    var exists : Boolean = false
//                    allBeaches.forEach { abeach ->
//                        if(beach.locationName == abeach.locationName)
//                        {
//                            exists = true
//                        }
//
//                        if(!exists)
//                        {
//                            allBeaches.add(beach)
//                        }
//                    }
//                    if(allBeaches?.filter{ it.locationName == beach.locationName }?.count() == 0){
//                        allBeaches.add(beach)
//                    }
                //}
                //
                (_context as MainActivity).addBeachesToMap(response.body())
            }

            override fun onFailure(call: Call<List<BeachModel>>, t: Throwable?) {
                // Log error here since request failed
            }
        })
    }
}

interface ApiEndpoints{

    @GET("api/beach")
    fun getBeaches(): Call<List<BeachModel>>
    @GET("api/beach/61cb6485f505f83a5677d142")
    fun getBeach(): Call<BeachModel>
}