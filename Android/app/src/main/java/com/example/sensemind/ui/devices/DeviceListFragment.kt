package com.example.sensemind.ui.devices

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.EditText
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout
import com.example.sensemind.R
import com.example.sensemind.api.RetrofitClient
import com.example.sensemind.models.DeviceRegisterRequest
import com.example.sensemind.repository.DataRepository
import com.example.sensemind.ui.ViewModelFactory
import com.example.sensemind.utils.SessionManager
import com.google.android.material.floatingactionbutton.FloatingActionButton

class DeviceListFragment : Fragment() {

    private lateinit var viewModel: DeviceViewModel
    private lateinit var sessionManager: SessionManager
    private lateinit var adapter: DeviceAdapter

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        val view = inflater.inflate(R.layout.fragment_device_list, container, false)

        sessionManager = SessionManager(requireContext())
        val apiService = RetrofitClient(requireContext()).getApiService()
        val repository = DataRepository(apiService)
        viewModel = ViewModelProvider(this, ViewModelFactory(repository)).get(DeviceViewModel::class.java)

        val rvDevices = view.findViewById<RecyclerView>(R.id.rvDevices)
        val swipeRefresh = view.findViewById<SwipeRefreshLayout>(R.id.swipeRefreshDevices)
        val fabAdd = view.findViewById<FloatingActionButton>(R.id.fabAddDevice)

        adapter = DeviceAdapter(emptyList(), sessionManager.getDeviceId()) { selected ->
            sessionManager.saveDeviceId(selected.id)
            Toast.makeText(context, "Selected: ${selected.name}", Toast.LENGTH_SHORT).show()
        }

        rvDevices.layoutManager = LinearLayoutManager(context)
        rvDevices.adapter = adapter

        swipeRefresh.setOnRefreshListener { viewModel.fetchMyDevices() }

        fabAdd.setOnClickListener { showAddDeviceDialog() }

        viewModel.devicesResult.observe(viewLifecycleOwner) { response ->
            swipeRefresh.isRefreshing = false
            if (response.isSuccessful) {
                adapter.updateDevices(response.body() ?: emptyList(), sessionManager.getDeviceId())
            }
        }

        viewModel.registerResult.observe(viewLifecycleOwner) { response ->
            if (response.isSuccessful) {
                Toast.makeText(context, "Device registered!", Toast.LENGTH_SHORT).show()
                viewModel.fetchMyDevices()
            } else {
                Toast.makeText(context, "Failed to register device", Toast.LENGTH_SHORT).show()
            }
        }

        viewModel.fetchMyDevices()

        return view
    }

    private fun showAddDeviceDialog() {
        val dialogView = LayoutInflater.from(context).inflate(R.layout.dialog_add_device, null)
        val etSerial = dialogView.findViewById<EditText>(R.id.etDeviceSerial)
        val etName = dialogView.findViewById<EditText>(R.id.etDeviceName)
        val etPass = dialogView.findViewById<EditText>(R.id.etDevicePassword)

        AlertDialog.Builder(requireContext())
            .setTitle("Register New Device")
            .setView(dialogView)
            .setPositiveButton("Register") { _, _ ->
                val serial = etSerial.text.toString()
                val name = etName.text.toString()
                val pass = etPass.text.toString()
                if (serial.isNotEmpty() && pass.isNotEmpty()) {
                    viewModel.registerDevice(DeviceRegisterRequest(serial, name, pass))
                }
            }
            .setNegativeButton("Cancel", null)
            .show()
    }
}
