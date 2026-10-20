package com.walksteadfast.app.data

data class Devotion(
    val date: String,
    val title: String,
    val verse: String,
    val body: String,
    val videoURL: String = "",
    val imageURL: String = ""
)

data class Product(
    val eyebrow: String,
    val title: String,
    val price: String,
    val blurb: String,
    val url: String
)

data class Social(
    val name: String,
    val url: String
)
