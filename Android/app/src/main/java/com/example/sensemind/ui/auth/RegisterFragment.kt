package com.example.sensemind.ui.auth

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import androidx.navigation.fragment.findNavController
import com.example.sensemind.R
import com.example.sensemind.api.RetrofitClient
import com.example.sensemind.models.RegisterRequest
import com.example.sensemind.repository.DataRepository
import com.example.sensemind.ui.ViewModelFactory

class RegisterFragment : Fragment() {

    private lateinit var viewModel: AuthViewModel

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        val view = inflater.inflate(R.layout.fragment_register, container, false)

        val apiService = RetrofitClient(requireContext()).getApiService()
        val repository = DataRepository(apiService)
        viewModel = ViewModelProvider(this, ViewModelFactory(repository)).get(AuthViewModel::class.java)

        val etUsername = view.findViewById<EditText>(R.id.etUsername)
        val etEmail = view.findViewById<EditText>(R.id.etEmail)
        val etPassword = view.findViewById<EditText>(R.id.etPassword)
        val btnRegister = view.findViewById<Button>(R.id.btnRegister)
        val progressBar = view.findViewById<View>(R.id.progressBar)

        btnRegister.setOnClickListener {
            val username = etUsername.text.toString()
            val email = etEmail.text.toString()
            val password = etPassword.text.toString()
            if (username.isNotEmpty() && email.isNotEmpty() && password.isNotEmpty()) {
                progressBar.visibility = View.VISIBLE
                btnRegister.isEnabled = false
                viewModel.register(RegisterRequest(username, email, password))
            } else {
                Toast.makeText(context, "Please fill all fields", Toast.LENGTH_SHORT).show()
            }
        }

        viewModel.registerResult.observe(viewLifecycleOwner) { response ->
            progressBar.visibility = View.GONE
            btnRegister.isEnabled = true
            if (response.isSuccessful) {
                Toast.makeText(context, "Registration successful. Please login.", Toast.LENGTH_LONG).show()
                findNavController().popBackStack()
            } else {
                Toast.makeText(context, "Registration failed: ${response.message()}", Toast.LENGTH_SHORT).show()
            }
        }

        return view
    }
}
