package com.example.sensemind.ui

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.example.sensemind.repository.DataRepository

class ViewModelFactory(private val repository: DataRepository) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(com.example.sensemind.ui.auth.AuthViewModel::class.java)) {
            return com.example.sensemind.ui.auth.AuthViewModel(repository) as T
        }
        if (modelClass.isAssignableFrom(com.example.sensemind.ui.dashboard.DashboardViewModel::class.java)) {
            return com.example.sensemind.ui.dashboard.DashboardViewModel(repository) as T
        }
        if (modelClass.isAssignableFrom(com.example.sensemind.ui.history.HistoryViewModel::class.java)) {
            return com.example.sensemind.ui.history.HistoryViewModel(repository) as T
        }
        if (modelClass.isAssignableFrom(com.example.sensemind.ui.devices.DeviceViewModel::class.java)) {
            return com.example.sensemind.ui.devices.DeviceViewModel(repository) as T
        }
        if (modelClass.isAssignableFrom(com.example.sensemind.ui.admin.AdminViewModel::class.java)) {
            return com.example.sensemind.ui.admin.AdminViewModel(repository) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}
