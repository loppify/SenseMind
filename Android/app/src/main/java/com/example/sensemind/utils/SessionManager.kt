package com.example.sensemind.utils

import android.content.Context
import android.content.SharedPreferences

class SessionManager(context: Context) {
    private val prefs: SharedPreferences = context.getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE)

    companion object {
        private const val PREF_NAME = "SenseMindPrefs"
        private const val KEY_TOKEN = "jwt_token"
        private const val KEY_DEVICE_ID = "device_id"
        private const val KEY_ADMIN_TOKEN = "admin_token"

        const val BASE_URL = "https://sense-mind-ffgpbxh4awgahxek.polandcentral-01.azurewebsites.net"
        }

        fun saveToken(token: String) {
        prefs.edit().putString(KEY_TOKEN, token).apply()
        }

        fun getToken(): String? {
        return prefs.getString(KEY_TOKEN, null)
        }

        fun saveAdminToken(token: String) {
        prefs.edit().putString(KEY_ADMIN_TOKEN, token).apply()
        }

        fun getAdminToken(): String? {
        return prefs.getString(KEY_ADMIN_TOKEN, null)
        }

        fun saveDeviceId(deviceId: Int) {
        prefs.edit().putInt(KEY_DEVICE_ID, deviceId).apply()
    }

    fun getDeviceId(): Int {
        return prefs.getInt(KEY_DEVICE_ID, 1)
    }

    fun clear() {
        prefs.edit().remove(KEY_TOKEN).apply()
    }
}
