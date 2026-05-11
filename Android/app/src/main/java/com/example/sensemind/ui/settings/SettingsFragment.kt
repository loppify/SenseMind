package com.example.sensemind.ui.settings

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import com.example.sensemind.R
import com.example.sensemind.utils.SessionManager

class SettingsFragment : Fragment() {

    private lateinit var sessionManager: SessionManager

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        val view = inflater.inflate(R.layout.fragment_settings, container, false)
        
        sessionManager = SessionManager(requireContext())

        val etDeviceId = view.findViewById<EditText>(R.id.etDeviceId)
        val etAdminToken = view.findViewById<EditText>(R.id.etAdminToken)
        val btnSave = view.findViewById<Button>(R.id.btnSaveSettings)
        val btnLogout = view.findViewById<Button>(R.id.btnLogout)
        val btnBack = view.findViewById<View>(R.id.btnBack)

        btnBack.setOnClickListener {
            findNavController().popBackStack()
        }

        // Load current values
        etDeviceId.setText(sessionManager.getDeviceId().toString())
        etAdminToken.setText(sessionManager.getAdminToken() ?: "")

        btnSave.setOnClickListener {
            val deviceIdStr = etDeviceId.text.toString()
            val adminToken = etAdminToken.text.toString()
            
            if (deviceIdStr.isNotEmpty()) {
                sessionManager.saveDeviceId(deviceIdStr.toInt())
            }
            sessionManager.saveAdminToken(adminToken)
            Toast.makeText(context, "Settings saved.", Toast.LENGTH_SHORT).show()
        }

        btnLogout.setOnClickListener {
            sessionManager.clear()
            findNavController().navigate(R.id.loginFragment)
        }

        return view
    }
}
