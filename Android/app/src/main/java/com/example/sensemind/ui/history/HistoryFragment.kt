package com.example.sensemind.ui.history

import android.graphics.Color
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.core.content.ContextCompat
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import com.example.sensemind.R
import com.example.sensemind.api.RetrofitClient
import com.example.sensemind.models.HistoryRecord
import com.example.sensemind.repository.DataRepository
import com.example.sensemind.ui.ViewModelFactory
import com.example.sensemind.utils.SessionManager
import com.github.mikephil.charting.charts.LineChart
import com.github.mikephil.charting.data.Entry
import com.github.mikephil.charting.data.LineData
import com.github.mikephil.charting.data.LineDataSet

class HistoryFragment : Fragment() {

    private lateinit var viewModel: HistoryViewModel
    private lateinit var sessionManager: SessionManager
    private lateinit var lineChart: LineChart

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        val view = inflater.inflate(R.layout.fragment_history, container, false)
        
        sessionManager = SessionManager(requireContext())
        val apiService = RetrofitClient(requireContext()).getApiService()
        val repository = DataRepository(apiService)
        viewModel = ViewModelProvider(this, ViewModelFactory(repository)).get(HistoryViewModel::class.java)

        lineChart = view.findViewById(R.id.lineChart)
        setupChart()

        viewModel.historyResult.observe(viewLifecycleOwner) { response ->
            if (response.isSuccessful) {
                val history = response.body() ?: emptyList()
                updateChart(history)
            }
        }

        viewModel.fetchHistory(sessionManager.getDeviceId())

        return view
    }

    private fun setupChart() {
        lineChart.description.isEnabled = false
        lineChart.setTouchEnabled(true)
        lineChart.setDrawGridBackground(false)
        lineChart.xAxis.granularity = 1f
        lineChart.axisLeft.apply {
            axisMinimum = 0f
            axisMaximum = 3.5f
            labelCount = 4
        }
        lineChart.axisRight.isEnabled = false
    }

    private fun updateChart(history: List<HistoryRecord>) {
        val entries = history.reversed().mapIndexed { index, record ->
            val value = when (record.classifiedState) {
                "Relaxed" -> 0f
                "Focused" -> 1f
                "Anxious" -> 2f
                "Stressed" -> 3f
                else -> 1f // Unknown as 1
            }
            Entry(index.toFloat(), value)
        }

        val dataSet = LineDataSet(entries, "Stress Level").apply {
            color = ContextCompat.getColor(requireContext(), R.color.primary)
            valueTextColor = Color.BLACK
            lineWidth = 3f
            circleRadius = 5f
            setCircleColor(ContextCompat.getColor(requireContext(), R.color.primary))
            setDrawValues(false)
            mode = LineDataSet.Mode.CUBIC_BEZIER
            setDrawFilled(true)
            fillColor = ContextCompat.getColor(requireContext(), R.color.primary)
            fillAlpha = 30
        }

        lineChart.data = LineData(dataSet)
        lineChart.invalidate()
    }
}
