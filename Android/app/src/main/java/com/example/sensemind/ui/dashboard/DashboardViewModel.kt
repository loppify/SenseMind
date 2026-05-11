package com.example.sensemind.ui.dashboard

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.sensemind.models.StateRecord
import com.example.sensemind.repository.DataRepository
import kotlinx.coroutines.launch
import retrofit2.Response

class DashboardViewModel(private val repository: DataRepository) : ViewModel() {

    private val _statusResult = MutableLiveData<Response<StateRecord>>()
    val statusResult: LiveData<Response<StateRecord>> = _statusResult

    fun fetchCurrentStatus(deviceId: Int) {
        viewModelScope.launch {
            try {
                val response = repository.getCurrentStatus(deviceId)
                _statusResult.value = response
            } catch (e: Exception) {
                // Handle error
            }
        }
    }
}
