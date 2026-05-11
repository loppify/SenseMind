package com.example.sensemind.ui.auth

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import androidx.navigation.fragment.findNavController
import com.example.sensemind.R
import com.example.sensemind.api.RetrofitClient
import com.example.sensemind.models.LoginRequest
import com.example.sensemind.repository.DataRepository
import com.example.sensemind.ui.ViewModelFactory
import com.example.sensemind.utils.SessionManager

class LoginFragment : Fragment() {

    private lateinit var viewModel: AuthViewModel
    private lateinit var sessionManager: SessionManager

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        val view = inflater.inflate(R.layout.fragment_login, container, false)
        
        sessionManager = SessionManager(requireContext())
        val apiService = RetrofitClient(requireContext()).getApiService()
        val repository = DataRepository(apiService)
        viewModel = ViewModelProvider(this, ViewModelFactory(repository)).get(AuthViewModel::class.java)

        val etUsername = view.findViewById<EditText>(R.id.etUsername)
        val etPassword = view.findViewById<EditText>(R.id.etPassword)
        val btnLogin = view.findViewById<Button>(R.id.btnLogin)
        val btnGoToRegister = view.findViewById<Button>(R.id.btnGoToRegister)
        val progressBar = view.findViewById<View>(R.id.progressBar)
        val tvLogo = view.findViewById<TextView>(R.id.tvLogo)

        tvLogo.setOnLongClickListener {
            findNavController().navigate(R.id.action_loginFragment_to_settingsFragment)
            true
        }

        btnLogin.setOnClickListener {
            val username = etUsername.text.toString()
            val password = etPassword.text.toString()
            if (username.isNotEmpty() && password.isNotEmpty()) {
                progressBar.visibility = View.VISIBLE
                btnLogin.isEnabled = false
                viewModel.login(LoginRequest(username, password))
            } else {
                Toast.makeText(context, "Please enter credentials", Toast.LENGTH_SHORT).show()
            }
        }

        btnGoToRegister.setOnClickListener {
            findNavController().navigate(R.id.action_loginFragment_to_registerFragment)
        }

        viewModel.loginResult.observe(viewLifecycleOwner) { response ->
            progressBar.visibility = View.GONE
            btnLogin.isEnabled = true
            if (response.isSuccessful) {
                response.body()?.let {
                    sessionManager.saveToken(it.accessToken)
                    findNavController().navigate(R.id.action_loginFragment_to_dashboardFragment)
                }
            } else {
                Toast.makeText(context, "Login failed: ${response.message()}", Toast.LENGTH_SHORT).show()
            }
        }

        return view
    }
}
