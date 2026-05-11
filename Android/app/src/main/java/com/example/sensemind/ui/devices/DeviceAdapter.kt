package com.example.sensemind.ui.devices

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.RadioButton
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.sensemind.R
import com.example.sensemind.models.DeviceResponse

class DeviceAdapter(
    private var devices: List<DeviceResponse>,
    private var selectedDeviceId: Int,
    private val onDeviceSelected: (DeviceResponse) -> Unit
) : RecyclerView.Adapter<DeviceAdapter.DeviceViewHolder>() {

    inner class DeviceViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val tvName: TextView = view.findViewById(R.id.tvDeviceName)
        val tvSerial: TextView = view.findViewById(R.id.tvDeviceSerial)
        val rbSelected: RadioButton = view.findViewById(R.id.rbSelected)

        fun bind(device: DeviceResponse) {
            tvName.text = device.name
            tvSerial.text = "Serial: ${device.serialId}"
            rbSelected.isChecked = device.id == selectedDeviceId
            
            itemView.setOnClickListener {
                selectedDeviceId = device.id
                onDeviceSelected(device)
                notifyDataSetChanged()
            }
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): DeviceViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_device, parent, false)
        return DeviceViewHolder(view)
    }

    override fun onBindViewHolder(holder: DeviceViewHolder, position: Int) {
        holder.bind(devices[position])
    }

    override fun getItemCount() = devices.size

    fun updateDevices(newDevices: List<DeviceResponse>, newSelectedId: Int) {
        devices = newDevices
        selectedDeviceId = newSelectedId
        notifyDataSetChanged()
    }
}
