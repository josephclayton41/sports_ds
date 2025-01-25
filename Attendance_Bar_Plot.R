# Load necessary libraries
library(ggplot2)
library(dplyr)
library(lubridate)

# Read the CSV file
file_path <- '/Users/joseph/Downloads/Kings Attendance DS Club/Kings_Attendance_Post_Covid.csv'
data <- read.csv(file_path)

# Ensure 'Date' column is in Date format
data$Date <- as.Date(data$Date)

# Extract year and month as a proper date object
data <- data %>%
  mutate(YearMonth = floor_date(Date, "month"))  # Creates a Date object for the first of each month

# Calculate average attendance for each month
monthly_avg <- data %>%
  group_by(YearMonth) %>%
  summarise(AverageAttend = mean(Attend., na.rm = TRUE)) %>%  # Calculate mean ignoring NA
  filter(!is.na(AverageAttend))  # Remove rows where AverageAttend is NA

# Ensure 'YearMonth' is ordered chronologically and factor levels are correct
monthly_avg$YearMonth <- factor(monthly_avg$YearMonth, levels = monthly_avg$YearMonth)

# Create the bar plot
ggplot(monthly_avg, aes(x = YearMonth, y = AverageAttend)) +
  geom_bar(stat = "identity", fill = "skyblue") +
  theme_minimal() +
  labs(title = "Average Attendance per Month",
       x = "Month",
       y = "Average Attendance") +
  scale_x_discrete(labels = function(x) format(as.Date(x), "%b %Y")) +  # Formatting the x-axis labels
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

