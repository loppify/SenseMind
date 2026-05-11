package com.example.sensemind.ui.admin

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import com.example.sensemind.R
import com.example.sensemind.api.RetrofitClient
import com.example.sensemind.repository.DataRepository
import com.example.sensemind.ui.ViewModelFactory
import com.example.sensemind.utils.SessionManager

class AdminFragment : Fragment() {

    private lateinit var viewModel: AdminViewModel
    private lateinit var sessionManager: SessionManager

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        val view = inflater.inflate(R.layout.fragment_admin, container, false)

        sessionManager = SessionManager(requireContext())
        val apiService = RetrofitClient(requireContext()).getApiService()
        val repository = DataRepository(apiService)
        viewModel = ViewModelProvider(this, ViewModelFactory(repository)).get(AdminViewModel::class.java)

        val btnExport = view.findViewById<Button>(R.id.btnExportData)
        val btnClear = view.findViewById<Button>(R.id.btnClearSystem)

        btnExport.setOnClickListener {
            val token = sessionManager.getAdminToken()
            if (token != null) {
                viewModel.exportData(token)
            } else {
                Toast.makeText(context, "Set Admin Token in Settings first", Toast.LENGTH_SHORT).show()
            }
        }

        btnClear.setOnClickListener {
            val token = sessionManager.getAdminToken()
            if (token != null) {
                showConfirmClearDialog(token)
            } else {
                Toast.makeText(context, "Set Admin Token in Settings first", Toast.LENGTH_SHORT).show()
            }
        }

        viewModel.clearResult.observe(viewLifecycleOwner) { response ->
            if (response.isSuccessful) {
                Toast.makeText(context, "System cleared successfully!", Toast.LENGTH_LONG).show()
            } else {
                Toast.makeText(context, "Unauthorized or Error", Toast.LENGTH_SHORT).show()
            }
        }

        viewModel.exportResult.observe(viewLifecycleOwner) { response ->
            if (response.isSuccessful) {
                Toast.makeText(context, "Data exported! (Check server console/logs)", Toast.LENGTH_LONG).show()
            } else {
                Toast.makeText(context, "Unauthorized or Error", Toast.LENGTH_SHORT).show()
            }
        }

        return view
    }

    private fun showConfirmClearDialog(token: String) {
        AlertDialog.Builder(requireContext())
            .setTitle("Clear System Data")
            .setMessage("Are you sure you want to delete ALL records? This cannot be undone.")
            .setPositiveButton("Clear Everything") { _, _ ->
                viewModel.clearSystem(token)
            }
            .setNegativeButton("Cancel", null)
            .show()
    }
}
