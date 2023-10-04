extern crate reqwest;
extern crate serde;
extern crate serde_json;

use std::collections::HashMap;
use reqwest::Error;
use serde::{Deserialize, Serialize};
use std::fs::File;
use std::io::Read;
use std::path::Path;

// Define a struct to deserialize the OpenStreetMap response
#[derive(Debug, Deserialize)]
struct OSMResponse {
    node: Vec<OSMElement>,
}

#[derive(Debug, Deserialize)]
struct OSMElement {
    id: i64,
    lat: f64,
    lon: f64,
    tag: Option<Vec<OSMTag>>,
}

#[derive(Debug, Deserialize)]
struct OSMTag {
    k: String,
    v: String,
}

#[derive(Debug, Serialize)]
struct OSMQuery{
    data: String,
}

// TODO: make into proper cli tool
#[tokio::main]
async fn main() -> Result<(), Error> {
    let response: String = { if Path::new("map_data.json").is_file() {
        // TODO: fix loading from local json
        println!("Loading map data from file");

        let mut file = File::open("map_data.json").unwrap();
        let mut response: String = String::new();
        file.read_to_string(&mut response).unwrap();
        response
    } else {
        println!("Querying map data from OverPass API");

        let osm_query = OSMQuery {
            data: r#"
                <osm-script>
                  <bbox-query s="45.130654" w="-63.355381" n="45.145196" e="-63.340095"/>
                  <print mode="meta"/>
                </osm-script>
            "#.to_string(),
        };
        // Send a request to the OpenStreetMap API to fetch roads within the specified area
        let osm_url = "https://overpass-api.de/api/interpreter";
        let client = reqwest::Client::new();
        client
            .post(osm_url)
            .form(&osm_query)
            .send().await?.text().await?
    }};

    let osm_data: OSMResponse = serde_xml_rs::from_str(&*response).unwrap();
    // println!("{:?}", osm_data);

    // Calculate the average distance between roads
    let mut prev_road_lat = 0.0;
    let mut prev_road_lon = 0.0;

    let mut total_distance = 0.0;
    let mut road_count = 0;

    for element in osm_data.node.iter() {
        if element.tag.is_some() {
            for tag in element.tag.as_ref().unwrap().iter() {
                if &tag.k == "highway" {
                    let road_lat1 = element.lat;
                    let road_lon1 = element.lon;

                    // Check if this is the first highway node encountered
                    if road_count == 0 {
                        prev_road_lat = road_lat1;
                        prev_road_lon = road_lon1;
                    } else {
                        // Calculate the distance between the current and previous highway nodes
                        let distance = haversine_distance(prev_road_lat, prev_road_lon, road_lat1, road_lon1);

                        total_distance += distance;
                    }

                    // Update the previous road's latitude and longitude
                    prev_road_lat = road_lat1;
                    prev_road_lon = road_lon1;

                    road_count += 1;
                    continue;
                }
            }
        }
    }

    if road_count > 0 {
        let average_distance = total_distance / road_count as f64;
        println!("Average distance between roads: {:.2} meters", average_distance);
    } else {
        println!("No roads found in the specified area.");
    }

    Ok(())
}

fn haversine_distance(lat1: f64, lon1: f64, lat2: f64, lon2: f64) -> f64 {
    const EARTH_RADIUS: f64 = 6371.0; // Radius of the Earth in kilometers

    // Convert latitude and longitude from degrees to radians
    let lat1_rad = lat1.to_radians();
    let lon1_rad = lon1.to_radians();
    let lat2_rad = lat2.to_radians();
    let lon2_rad = lon2.to_radians();

    // Calculate differences between coordinates
    let delta_lat = lat2_rad - lat1_rad;
    let delta_lon = lon2_rad - lon1_rad;

    // Haversine formula
    let a = (delta_lat / 2.0).sin().powi(2)
        + lat1_rad.cos() * lat2_rad.cos() * (delta_lon / 2.0).sin().powi(2);
    let c = 2.0 * a.sqrt().atan2((1.0 - a).sqrt());

    // Calculate the distance
    let distance = EARTH_RADIUS * c;
    distance
}

