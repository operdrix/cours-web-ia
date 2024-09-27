<template>
    <v-container>
        <v-row>
            <!-- Formulaire d'ajout/modification -->
            <v-col>
                <v-card class="pa-3 ma-2">
                    <v-card-title class="headline">{{
                        editMode
                            ? "Modifier un appartement"
                            : "Ajouter un appartement"
                    }}</v-card-title>
                    <v-form @submit.prevent="submitForm">
                        <v-select
                            v-model="form.city"
                            :items="['Paris', 'Lyon', 'Marseille']"
                            label="Ville"
                            required
                        ></v-select>
                        <v-text-field
                            v-model.number="form.number_of_rooms"
                            label="Nombre de pièces"
                            type="number"
                            required
                        ></v-text-field>
                        <v-text-field
                            v-model.number="form.area"
                            label="Surface"
                            type="number"
                            required
                        ></v-text-field>
                        <v-row>
                            <v-col>
                                <v-text-field
                                    v-model.number="form.years_of_construction"
                                    label="Année de construction"
                                    type="number"
                                    required
                                ></v-text-field>
                            </v-col>
                            <v-col>
                                <p v-if="!editMode && form.city">
                                    <v-btn
                                        @click="getPredictionYear"
                                        color="primary"
                                    >
                                        Prédire de l'année
                                    </v-btn>
                                </p>
                            </v-col>
                        </v-row>

                        <v-row>
                            <v-col cols="3">
                                <v-checkbox
                                    v-model="form.have_balcony"
                                    label="Balcon"
                                    value="1"
                                ></v-checkbox>
                            </v-col>
                            <v-col cols="3">
                                <p v-if="!editMode && form.city && form.price">
                                    <v-btn
                                        @click="getPredictionHaveBalcony"
                                        color="primary"
                                    >
                                        Prédire de balcon </v-btn
                                    ><br />
                                    {{
                                        predictedHaveBalcony !== null
                                            ? predictedHaveBalcony
                                                ? "Avec balcon"
                                                : "Sans balcon"
                                            : ""
                                    }}
                                </p>
                            </v-col>
                            <v-col cols="3">
                                <v-checkbox
                                    v-model="form.have_garage"
                                    label="Garage"
                                    value="1"
                                ></v-checkbox>
                            </v-col>
                            <v-col cols="3">
                                <p v-if="!editMode && form.city && form.price">
                                    <v-btn
                                        @click="getPredictionHaveGarage"
                                        color="primary"
                                    >
                                        Prédire de garage </v-btn
                                    ><br />
                                    {{
                                        predictedHaveGarage !== null
                                            ? predictedHaveGarage
                                                ? "Avec garage"
                                                : "Sans garage"
                                            : ""
                                    }}
                                </p>
                            </v-col>
                        </v-row>
                        <v-text-field
                            v-model.number="form.price"
                            label="Prix"
                            type="number"
                            required
                        ></v-text-field>
                        <v-row>
                            <v-col>
                                <v-rating
                                    v-model="form.rating"
                                    label="Note"
                                    dense
                                    color="yellow"
                                    background-color="grey"
                                    size="24"
                                ></v-rating>
                            </v-col>
                            <v-col>
                                <p
                                    v-if="
                                        !editMode &&
                                        form.city &&
                                        form.area &&
                                        form.price
                                    "
                                >
                                    <v-btn
                                        @click="getPredictionRating"
                                        color="primary"
                                    >
                                        Prédire de la note
                                    </v-btn>
                                </p>
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-col cols="6">
                                <v-btn type="submit" color="success" block>
                                    {{ editMode ? "Mettre à jour" : "Ajouter" }}
                                </v-btn>
                            </v-col>
                            <v-col cols="6" v-if="editMode">
                                <v-btn @click="resetForm" color="error" block>
                                    Annuler
                                </v-btn>
                            </v-col>
                        </v-row>
                    </v-form>
                </v-card>
            </v-col>
        </v-row>
        <v-row>
            <!-- Liste des appartements -->
            <v-col>
                <v-card>
                    <v-card-title class="headline"
                        >Liste d'appartements</v-card-title
                    >
                    <v-simple-table class="styled-table">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Ville</th>
                                <th>Pièces</th>
                                <th>Surface (m²)</th>
                                <th>Année</th>
                                <th>Balcon</th>
                                <th>Garage</th>
                                <th>Prix (€)</th>
                                <th>Note</th>
                                <th>Qualité / Prix</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="suite in apartments" :key="suite.id">
                                <td>{{ suite.id }}</td>
                                <td>{{ suite.city }}</td>
                                <td>{{ suite.number_of_rooms }}</td>
                                <td>{{ suite.area }} m²</td>
                                <td>{{ suite.years_of_construction }}</td>
                                <td>
                                    {{
                                        suite.have_balcony == 1 ? "Oui" : "Non"
                                    }}
                                </td>
                                <td>
                                    {{ suite.have_garage == 1 ? "Oui" : "Non" }}
                                </td>
                                <td>
                                    {{
                                        new Intl.NumberFormat("fr-FR", {
                                            style: "currency",
                                            currency: "EUR",
                                        }).format(suite.price)
                                    }}
                                </td>
                                <td>
                                    <v-rating
                                        v-model="suite.rating"
                                        label="Note"
                                        dense
                                        length="5"
                                        readonly
                                        color="yellow"
                                        background-color="grey"
                                        size="16"
                                    ></v-rating>
                                </td>
                                <td>
                                    <v-chip
                                        :color="
                                            getCategoryColor(suite.category)
                                        "
                                        dark
                                    >
                                        {{
                                            suite.category === "low"
                                                ? "Bas"
                                                : suite.category === "medium"
                                                ? "Moyen"
                                                : suite.category === "high"
                                                ? "Haut"
                                                : suite.category === "scam"
                                                ? "Arnaque"
                                                : "Inconnu"
                                        }}
                                    </v-chip>
                                </td>
                                <td>
                                    <v-btn
                                        @click="editSuite(suite)"
                                        color="primary"
                                        class="action-btn"
                                        density="comfortable"
                                        size="small"
                                        icon="mdi-pencil"
                                    >
                                    </v-btn>
                                    <v-btn
                                        @click="deleteSuite(suite.id)"
                                        color="error"
                                        class="action-btn"
                                        density="comfortable"
                                        size="small"
                                        icon="mdi-delete"
                                    >
                                    </v-btn>
                                </td>
                            </tr>
                        </tbody>
                    </v-simple-table>
                </v-card>
                <!-- Pagination -->
                <v-pagination
                    v-model="currentPage"
                    :length="totalPages"
                    :total-visible="7"
                ></v-pagination>
            </v-col>
        </v-row>
    </v-container>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import axios from "axios";

const apartments = ref([]);
const currentPage = ref(1);
const totalPages = ref(0);
const itemsPerPage = ref(50);

const fetchApartments = async () => {
    console.log("fetching apartments");

    try {
        const response = await axios.get("http://localhost:3002/suites", {
            params: {
                page: currentPage.value,
                limit: itemsPerPage.value,
            },
        });
        totalPages.value = response.data.totalPages;
        apartments.value = response.data.suites;
    } catch (error) {
        console.error(error);
    }
};
watch(currentPage, fetchApartments);

onMounted(async () => {
    await fetchApartments();

    // Entraînement des prédictions
    try {
        await axios.post("http://localhost:8000/train");
    } catch (error) {
        console.error(error);
    }
});

const form = ref({
    id: null,
    city: "",
    number_of_rooms: "",
    area: "",
    years_of_construction: "",
    have_balcony: false,
    have_garage: false,
    price: "",
    rating: 0,
});

const editMode = ref(false);

const getCategoryColor = (category) => {
    switch (category) {
        case "low":
            return "green";
        case "medium":
            return "orange";
        case "high":
            return "red";
        case "scam":
            return "purple";
        default:
            return "grey";
    }
};

const submitForm = async () => {
    if (editMode.value) {
        try {
            await axios.patch(
                `http://localhost:3002/suites/${form.value.id}`,
                form.value
            );
            const index = suites.value.findIndex(
                (suite) => suite.id === form.value.id
            );
            if (index !== -1) {
                suites.value[index] = { ...form.value };
            }
            resetForm();
        } catch (error) {
            console.error(error);
        }
    } else {
        try {
            const response = await axios.post(
                "http://localhost:3002/suites",
                form.value
            );
            form.value.id = response.data.id;
            suites.value.push({ ...form.value });
            resetForm();
        } catch (error) {
            console.error(error);
        }
    }
};

const editSuite = (suite) => {
    form.value = { ...suite };
    editMode.value = true;
};

const deleteSuite = async (id) => {
    try {
        await axios.delete(`http://localhost:3002/suites/${id}`);
        suites.value = suites.value.filter((suite) => suite.id !== id);
    } catch (error) {
        console.error(error);
    }
};

const resetForm = () => {
    form.value = {
        id: null,
        city: "",
        number_of_rooms: "",
        area: "",
        years_of_construction: "",
        have_balcony: false,
        have_garage: false,
        price: "",
        rating: 0,
    };
    editMode.value = false;
};

const predictedRating = ref(null);
const predictedYear = ref(null);
const predictedHaveBalcony = ref(null);
const predictedHaveGarage = ref(null);

const getPredictionRating = async () => {
    try {
        const response = await axios.post(
            "http://localhost:8000/predict-rating",
            {
                city: form.value.city,
                area: form.value.area,
                price: form.value.price,
            }
        );
        form.value.rating = Math.min(response.data.predicted_rating, 5);
        predictedRating.value = form.value.rating;
    } catch (error) {
        console.error(error);
    }
};
const getPredictionYear = async () => {
    try {
        const response = await axios.post(
            "http://localhost:8000/predict-years-of-construction",
            {
                city: form.value.city,
            }
        );
        form.value.years_of_construction =
            response.data.predicted_years_of_construction;
        predictedYear.value = form.value.years_of_construction;
    } catch (error) {
        console.error(error);
    }
};
const getPredictionHaveBalcony = async () => {
    try {
        const response = await axios.post(
            "http://localhost:8000/predict-have-balcony",
            {
                city: form.value.city,
                price: form.value.price,
            }
        );
        predictedHaveBalcony.value = response.data.predicted_have_balcony;
    } catch (error) {
        console.error(error);
    }
};
const getPredictionHaveGarage = async () => {
    try {
        const response = await axios.post(
            "http://localhost:8000/predict-have-garage",
            {
                city: form.value.city,
                price: form.value.price,
            }
        );
        predictedHaveGarage.value = response.data.predicted_have_garage;
    } catch (error) {
        console.error(error);
    }
};
</script>

<style scoped>
.styled-table {
    width: 100%;
    border-collapse: collapse;
}

.styled-table th,
.styled-table td {
    border: 1px solid #ddd;
    padding: 8px;
}

.styled-table th {
    background-color: #f2f2f2;
    text-align: left;
}

.styled-table tr:nth-child(even) {
    background-color: #f9f9f9;
}

.styled-table tr:hover {
    background-color: #f1f1f1;
}

.action-btn {
    margin-right: 5px;
    width: 25px;
}

.table-responsive {
    overflow-x: auto;
}
</style>
