package com.example.sensemind.models

import com.google.gson.annotations.SerializedName

data class DeviceRegisterRequest(
    @SerializedName("device_serial_id") val serialId: String,
    @SerializedName("name") val name: String,
    @SerializedName("device_password") val devicePassword: String
)

data class DeviceResponse(
    @SerializedName("id") val id: Int,
    @SerializedName("device_serial_id") val serialId: String,
    @SerializedName("name") val name: String
)
