package com.example.sensemind.api

import com.example.sensemind.models.*
import retrofit2.Response
import retrofit2.http.*

interface ApiService {
    @POST("api/v1/auth/register")
    suspend fun register(@Body request: RegisterRequest): Response<MessageResponse>

    @POST("api/v1/auth/login")
    suspend fun login(@Body request: LoginRequest): Response<LoginResponse>

    @GET("api/v1/status/current/{device_id}")
    suspend fun getCurrentStatus(@Path("device_id") deviceId: Int): Response<StateRecord>

    @GET("api/v1/history/{device_id}")
    suspend fun getHistory(@Path("device_id") deviceId: Int): Response<List<HistoryRecord>>

    // Device Management
    @POST("api/v1/devices/register")
    suspend fun registerDevice(@Body request: DeviceRegisterRequest): Response<MessageResponse>

    @GET("api/v1/devices/my")
    suspend fun getMyDevices(): Response<List<DeviceResponse>>

    // Admin Features
    @GET("api/v1/admin/export/data")
    suspend fun exportData(@Header("X-Admin-Token") adminToken: String): Response<okhttp3.ResponseBody>

    @DELETE("api/v1/admin/system/clear")
    suspend fun clearSystem(@Header("X-Admin-Token") adminToken: String): Response<MessageResponse>
}
