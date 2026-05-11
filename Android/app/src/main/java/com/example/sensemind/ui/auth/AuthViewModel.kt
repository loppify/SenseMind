package com.example.sensemind.ui.auth

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.sensemind.models.LoginRequest
import com.example.sensemind.models.LoginResponse
import com.example.sensemind.models.RegisterRequest
import com.example.sensemind.repository.DataRepository
import kotlinx.coroutines.launch
import retrofit2.Response

class AuthViewModel(private val repository: DataRepository) : ViewModel() {

    private val _loginResult = MutableLiveData<Response<LoginResponse>>()
    val loginResult: LiveData<Response<LoginResponse>> = _loginResult

    private val _registerResult = MutableLiveData<Response<com.example.sensemind.models.MessageResponse>>()
    val registerResult: LiveData<Response<com.example.sensemind.models.MessageResponse>> = _registerResult

    fun login(request: LoginRequest) {
        viewModelScope.launch {
            try {
                val response = repository.login(request)
                _loginResult.value = response
            } catch (e: Exception) {
                // Handle error
            }
        }
    }

    fun register(request: RegisterRequest) {
        viewModelScope.launch {
            try {
                val response = repository.register(request)
                _registerResult.value = response
            } catch (e: Exception) {
                // Handle error
            }
        }
    }
}
