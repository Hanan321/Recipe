package com.hfad.myapplication;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    //Call onDisplayCafeLate() when button clicked
    public void onDisplayCafeLate(View view){

        // Use Intent to call the second activity
        Intent intent = new Intent(this, CafeLatte.class);
        startActivity(intent);

    }

    public void onDisplayScrambledEggs(View view){
        Intent intent = new Intent(this, ScrambledEggs.class);
        startActivity(intent);

    }

    public void onDisplayGardenSalad(View view){
        Intent intent = new Intent(this,GardenSalad.class);
        startActivity(intent);
    }
}
