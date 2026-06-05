import sys
import math
import rosbag2_py
from rclpy.serialization import deserialize_message
from rosidl_runtime_py.utilities import get_message

def analyze_f1tenth_bag(bag_path: str):
    print(f"--- Processing F1TENTH Dataset: {bag_path} ---")
    
    # 1. Initialize the High-Performance Sequential Reader
    reader = rosbag2_py.SequentialReader()
    
    # Automatically detect if bag is mcap or sqlite3
    storage_id = "mcap" if "mcap" in bag_path else "sqlite3"
    
    storage_options = rosbag2_py.StorageOptions(uri=bag_path, storage_id=storage_id)
    converter_options = rosbag2_py.ConverterOptions(
        input_serialization_format="cdr",
        output_serialization_format="cdr"
    )
    
    try:
        reader.open(storage_options, converter_options)
    except Exception as e:
        print(f"Error opening bag: {e}")
        return

    # 2. Map topics to types available in the local environment
    topic_types = reader.get_all_topics_and_types()
    type_map = {topic.name: topic.type for topic in topic_types}
    
    # Metrics to track
    max_linear_velocity = 0.0
    anomaly_count = 0
    total_messages = 0
    
    print("\n[Parsing high-frequency data streams...]")
    
    # 3. Read sequential messages directly from storage
    while reader.has_next():
        topic, data, timestamp = reader.read_next()
        total_messages += 1
        
        # Track Odometry for velocity and slip anomalies
        if topic == "/ego_racecar/odom" or topic == "/odom":
            msg_type = get_message(type_map[topic])
            odom_msg = deserialize_message(data, msg_type)
            
            # Read velocities
            vx = odom_msg.twist.twist.linear.x
            vy = odom_msg.twist.twist.linear.y
            speed = math.sqrt(vx**2 + vy**2)
            
            if speed > max_linear_velocity:
                max_linear_velocity = speed
                
            # Dynamic Anomaly: Calculate Slip Angle (Beta)
            # If side-slip is massive while moving fast, the vehicle is drifting/crashing
            if speed > 1.0: 
                slip_angle = math.atan2(vy, vx)
                if abs(slip_angle) > 0.4:  # > ~23 degrees of lateral slip
                    anomaly_count += 1

    # 4. Compile Race Metrics Report
    print("\n================ RACE ENGINEER REPORT ================")
    print(f"Processed Message Count : {total_messages}")
    print(f"Top Speed Clocked       : {max_linear_velocity:.2f} m/s ({max_linear_velocity * 3.6:.1f} km/h)")
    print(f"Lateral Slip Anomalies  : {anomaly_count} events detected")
    if anomaly_count > 50:
        print("Status Evaluation       : High probability of loss-of-control or spinout.")
    else:
        print("Status Evaluation       : Clean run. Traction control optimal.")
    print("=======================================================")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 bag_analyzer.py <path_to_rosbag_folder_or_mcap>")
    else:
        analyze_f1tenth_bag(sys.argv[1])