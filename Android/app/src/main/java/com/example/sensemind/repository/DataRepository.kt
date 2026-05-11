package com.example.sensemind.repository

import com.example.sensemind.api.ApiService
import com.example.sensemind.models.*
import retrofit2.Response

class DataRepository(private val apiService: ApiService) {
    suspend fun login(request: LoginRequest) = apiService.login(request)
    suspend fun register(request: RegisterRequest) = apiService.register(request)
    suspend fun getCurrentStatus(deviceId: Int) = apiService.getCurrentStatus(deviceId)
    suspend fun getHistory(deviceId: Int) = apiService.getHistory(deviceId)
    
    // New
    suspend fun registerDevice(request: DeviceRegisterRequest) = apiService.registerDevice(request)
    suspend fun getMyDevices() = apiService.getMyDevices()
    suspend fun exportData(adminToken: String) = apiService.exportData(adminToken)
    suspend fun clearSystem(adminToken: String) = apiService.clearSystem(adminToken)
}
