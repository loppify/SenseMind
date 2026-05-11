package com.example.sensemind.ui.dashboard

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.core.content.ContextCompat
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout
import com.example.sensemind.R
import com.example.sensemind.api.RetrofitClient
import com.example.sensemind.repository.DataRepository
import com.example.sensemind.ui.ViewModelFactory
import com.example.sensemind.utils.SessionManager

class DashboardFragment : Fragment() {

    private lateinit var viewModel: DashboardViewModel
    private lateinit var sessionManager: SessionManager

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        val view = inflater.inflate(R.layout.fragment_dashboard, container, false)
        
        sessionManager = SessionManager(requireContext())
        val apiService = RetrofitClient(requireContext()).getApiService()
        val repository = DataRepository(apiService)
        viewModel = ViewModelProvider(this, ViewModelFactory(repository)).get(DashboardViewModel::class.java)

        val tvCurrentState = view.findViewById<TextView>(R.id.tvCurrentState)
        val tvRecommendation = view.findViewById<TextView>(R.id.tvRecommendation)
        val tvHrvValue = view.findViewById<TextView>(R.id.tvHrvValue)
        val tvGsrValue = view.findViewById<TextView>(R.id.tvGsrValue)
        val swipeRefresh = view.findViewById<SwipeRefreshLayout>(R.id.swipeRefresh)

        swipeRefresh.setOnRefreshListener {
            viewModel.fetchCurrentStatus(sessionManager.getDeviceId())
        }

        viewModel.statusResult.observe(viewLifecycleOwner) { response ->
            swipeRefresh.isRefreshing = false
            if (response.isSuccessful) {
                val record = response.body()
                tvCurrentState.text = record?.classifiedState
                tvRecommendation.text = record?.recommendation ?: "No recommendations yet."
                tvHrvValue.text = record?.hrvScore?.toString() ?: "--"
                tvGsrValue.text = record?.gsrScore?.toString() ?: "--"
                
                val color = when (record?.classifiedState) {
                    "Stressed" -> ContextCompat.getColor(requireContext(), R.color.state_stressed)
                    "Anxious" -> ContextCompat.getColor(requireContext(), R.color.state_anxious)
                    "Relaxed" -> ContextCompat.getColor(requireContext(), R.color.state_relaxed)
                    "Focused" -> ContextCompat.getColor(requireContext(), R.color.state_focused)
                    else -> ContextCompat.getColor(requireContext(), R.color.black)
                }
                tvCurrentState.setTextColor(color)
            } else {
                tvCurrentState.text = "Error"
                tvRecommendation.text = "Could not fetch data. Check your connection and Device ID."
            }
        }

        viewModel.fetchCurrentStatus(sessionManager.getDeviceId())

        return view
    }
}
