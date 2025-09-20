package models

import (
	"time"
)

// Common Objects

type LatLong struct {
	Lat     float64 `json:"lat"`
	Long    float64 `json:"long"`
	Address *string `json:"address,omitempty"`
}

type EnvironmentalConditions struct {
	SoilQuality       *string  `json:"soil_quality,omitempty"`
	Moisture          *float64 `json:"moisture,omitempty"`
	Temperature       *float64 `json:"temperature,omitempty"`
	Humidity          *float64 `json:"humidity,omitempty"`
	WeatherConditions *string  `json:"weather_conditions,omitempty"`
	IrrigationMethod  *string  `json:"irrigation_method,omitempty"`
}

type FarmingInputs struct {
	Fertilizers      *string `json:"fertilizers,omitempty"`
	PesticidesUsed   *string `json:"pesticides_used,omitempty"`
	OrganicCertified bool    `json:"organic_certified"`
}

type PermitCompliance struct {
	PermitID   string     `json:"permit_id"`
	PermitType string     `json:"permit_type"`
	Issuer     string     `json:"issuer"`
	ValidUntil *time.Time `json:"valid_until,omitempty"`
}

type FarmerDetails struct {
	ProfileID string    `json:"profile_id"`
	BatchID   string    `json:"batch_id"`
	CropID    string    `json:"crop_id"`
	StartTime time.Time `json:"start_time"`
}

// Collection Event
type CollectionEvent struct {
	BatchID     string                    `json:"batch_id"`
	ProfileID   string                    `json:"profile_id"`
	CropID      string                    `json:"crop_id"`
	Location    LatLong                   `json:"location"`
	StartDate   time.Time                 `json:"start_date"`
	HarvestDate time.Time                 `json:"harvest_date"`
	Environment *EnvironmentalConditions  `json:"environment,omitempty"`
	Inputs      *FarmingInputs            `json:"inputs,omitempty"`
	Permits     *[]PermitCompliance       `json:"permits,omitempty"`
}

// Transport Event
type TransportEvent struct {
	TransportID         string                    `json:"transport_id"`
	BatchID             string                    `json:"batch_id"`
	ProvenanceFhirURL   string                    `json:"provenance_fhir_url"`
	ProfileID           string                    `json:"profile_id"`
	Origin              LatLong                   `json:"origin"`
	Destination         LatLong                   `json:"destination"`
	StartTime           time.Time                 `json:"start_time"`
	EndTime             time.Time                 `json:"end_time"`
	TransportConditions *EnvironmentalConditions  `json:"transport_conditions,omitempty"`
	Sealed              bool                      `json:"sealed"`
	Notes               *string                   `json:"notes,omitempty"`
}

// Processing Event
type ProcessingEvent struct {
	ProcessingID       string                    `json:"processing_id"`
	BatchID            string                    `json:"batch_id"`
	ProfileID          string                    `json:"profile_id"`
	CompanyLocation    LatLong                   `json:"company_location"`
	ProcessesApplied   []string                  `json:"processes_applied"`
	ProcessConditions  *EnvironmentalConditions  `json:"process_conditions,omitempty"`
	StartTime          time.Time                 `json:"start_time"`
	EndTime            time.Time                 `json:"end_time"`
	VisualInspection   *[]string                 `json:"visual_inspection,omitempty"`
	EquipmentCleaned   bool                      `json:"equipment_cleaned"`
	Notes              *string                   `json:"notes,omitempty"`
}

// Quality Test
type TestResults struct {
	TestID         string  `json:"test_id"`
	TestType       string  `json:"test_type"`
	Value          float64 `json:"value"`
	Units          string  `json:"units"`
	ReferenceRange *string `json:"reference_range,omitempty"`
	Passed         bool    `json:"passed"`
}

type QualityTest struct {
	TestID                  string        `json:"test_id"`
	BatchID                 string        `json:"batch_id"`
	ProfileID               string        `json:"profile_id"`
	DateOfTest              time.Time     `json:"date_of_test"`
	TestResults             []TestResults `json:"test_results"`
	CertificationReportURL  *string       `json:"certification_report_url,omitempty"`
	Notes                   *string       `json:"notes,omitempty"`
}

// Manufacturing Event
type IngredientsModel struct {
	IngredientID string  `json:"ingredient_id"`
	Name         string  `json:"name"`
	Quantity     float64 `json:"quantity"`
	Units        string  `json:"units"`
}

type ManufacturingEvent struct {
	ManufacturingID  string             `json:"manufacturing_id"`
	ProductName      string             `json:"product_name"`
	BatchIDsUsed     string             `json:"batch_ids_used"`
	ManufacturerID   string             `json:"manufacturer_id"`
	ManufactureDate  time.Time          `json:"manufacture_date"`
	Ingredients      []IngredientsModel `json:"ingredients"`
	GMPCompliance    bool               `json:"GMP_compliance"`
	TestIDs          *[]string          `json:"test_ids,omitempty"`
	FinalQuantity    float64            `json:"final_quantity"`
	Notes            *string            `json:"notes,omitempty"`
}

// Packing Event
type PackingEvent struct {
	PackingID     string     `json:"packing_id"`
	PackingFhirURL string    `json:"packing_fhir_url"`
	ManufacturingID string   `json:"manufacturing_id"`
	PackerID      string     `json:"packer_id"`
	DateOfPacking time.Time  `json:"date_of_packing"`
	QrCodeURL     *string    `json:"qr_code_url,omitempty"`
	Notes         *string    `json:"notes,omitempty"`
}

// Event interface for polymorphic behavior
type Event interface {
	GetEventType() string
}

// Implement the interface for each event type
func (c CollectionEvent) GetEventType() string   { return "collection" }
func (t TransportEvent) GetEventType() string    { return "transport" }
func (p ProcessingEvent) GetEventType() string   { return "processing" }
func (q QualityTest) GetEventType() string       { return "quality_test" }
func (m ManufacturingEvent) GetEventType() string { return "manufacturing" }
func (p PackingEvent) GetEventType() string      { return "packing" }

type QrCodeData struct {
	FromID    string      `json:"from_id"`
	ToID      string      `json:"to_id"`
	BatchID   string      `json:"batch_id"`
	FromRole  string      `json:"from_role"`
	ToRole    string      `json:"to_role"`
	StartTime *time.Time  `json:"start_time,omitempty"`
	Event     interface{} `json:"event"` // Can hold any of the event types
}
