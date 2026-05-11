package com.example.sensemind.ui.devices

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.sensemind.models.DeviceRegisterRequest
import com.example.sensemind.models.DeviceResponse
import com.example.sensemind.models.MessageResponse
import com.example.sensemind.repository.DataRepository
import kotlinx.coroutines.launch
import retrofit2.Response

class DeviceViewModel(private val repository: DataRepository) : ViewModel() {

    private val _devicesResult = MutableLiveData<Response<List<DeviceResponse>>>()
    val devicesResult: LiveData<Response<List<DeviceResponse>>> = _devicesResult

    private val _registerResult = MutableLiveData<Response<MessageResponse>>()
    val registerResult: LiveData<Response<MessageResponse>> = _registerResult

    fun fetchMyDevices() {
        viewModelScope.launch {
            try {
                val response = repository.getMyDevices()
                _devicesResult.value = response
            } catch (e: Exception) {
                // Handle error
            }
        }
    }

    fun registerDevice(request: DeviceRegisterRequest) {
        viewModelScope.launch {
            try {
                val response = repository.registerDevice(request)
                _registerResult.value = response
            } catch (e: Exception) {
                // Handle error
            }
        }
    }
}
