package com.example.sensemind.ui.history

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.sensemind.models.HistoryRecord
import com.example.sensemind.repository.DataRepository
import kotlinx.coroutines.launch
import retrofit2.Response

class HistoryViewModel(private val repository: DataRepository) : ViewModel() {

    private val _historyResult = MutableLiveData<Response<List<HistoryRecord>>>()
    val historyResult: LiveData<Response<List<HistoryRecord>>> = _historyResult

    fun fetchHistory(deviceId: Int) {
        viewModelScope.launch {
            try {
                val response = repository.getHistory(deviceId)
                _historyResult.value = response
            } catch (e: Exception) {
                // Handle error
            }
        }
    }
}
