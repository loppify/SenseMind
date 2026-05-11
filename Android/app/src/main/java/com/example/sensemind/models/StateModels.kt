package com.example.sensemind.models

import com.google.gson.annotations.SerializedName

data class StateRecord(
    @SerializedName("timestamp") val timestamp: String,
    @SerializedName("classified_state") val classifiedState: String,
    @SerializedName("hrv_score") val hrvScore: Float,
    @SerializedName("gsr_score") val gsrScore: Float,
    @SerializedName("recommendation") val recommendation: String?
)

data class HistoryRecord(
    @SerializedName("timestamp") val timestamp: String,
    @SerializedName("classified_state") val classifiedState: String,
    @SerializedName("hrv_score") val hrvScore: Float,
    @SerializedName("gsr_score") val gsrScore: Float
)
