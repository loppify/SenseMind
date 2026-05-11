package com.example.sensemind.ui.admin

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.sensemind.models.MessageResponse
import com.example.sensemind.repository.DataRepository
import kotlinx.coroutines.launch
import okhttp3.ResponseBody
import retrofit2.Response

class AdminViewModel(private val repository: DataRepository) : ViewModel() {

    private val _clearResult = MutableLiveData<Response<MessageResponse>>()
    val clearResult: LiveData<Response<MessageResponse>> = _clearResult

    private val _exportResult = MutableLiveData<Response<ResponseBody>>()
    val exportResult: LiveData<Response<ResponseBody>> = _exportResult

    fun clearSystem(token: String) {
        viewModelScope.launch {
            try {
                val response = repository.clearSystem(token)
                _clearResult.value = response
            } catch (e: Exception) {
                // Handle error
            }
        }
    }

    fun exportData(token: String) {
        viewModelScope.launch {
            try {
                val response = repository.exportData(token)
                _exportResult.value = response
            } catch (e: Exception) {
                // Handle error
            }
        }
    }
}
