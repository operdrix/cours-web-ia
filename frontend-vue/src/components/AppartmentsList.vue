<template>
    <v-container>
        <v-row>
            <v-col cols="9">
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
                            <tr v-for="suite in suites" :key="suite.id">
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
                                        length="5"
                                        readonly
                                        color="yellow"
                                        background-color="grey"
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
            </v-col>
            <v-col cols="3">
                <v-card style="padding: 10px">
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
                        <v-text-field
                            v-model.number="form.years_of_construction"
                            label="Année de construction"
                            type="number"
                            required
                        ></v-text-field>
                        <v-row>
                            <v-col cols="6">
                                <v-checkbox
                                    v-model="form.have_balcony"
                                    label="Balcon"
                                    value="1"
                                ></v-checkbox>
                            </v-col>
                            <v-col cols="6">
                                <v-checkbox
                                    v-model="form.have_garage"
                                    label="Garage"
                                    value="1"
                                ></v-checkbox>
                            </v-col>
                        </v-row>
                        <v-text-field
                            v-model.number="form.price"
                            label="Prix"
                            type="number"
                            required
                        ></v-text-field>
                        <v-rating
                            v-model="form.rating"
                            label="Note"
                            dense
                            color="yellow"
                            background-color="grey"
                        ></v-rating>

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
    </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const suites = ref([]);

onMounted(async () => {
    try {
        const response = await axios.get("http://localhost:3002/suites");
        suites.value = response.data.slice(0, 100);
    } catch (error) {
        console.error(error);
    }

    // entrainement des prédictions
    try {
        await axios.post("http://localhost:8000/train");
    } catch (error) {
        console.error(error);
    }
});

const form = ref({
    id: null,
    nbRooms: "",
    surface: "",
    nbWindows: "",
    price: "",
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

// Ajouter ou mettre à jour un appartement
const submitForm = async () => {
    if (editMode.value) {
        try {
            await axios.patch(`http://localhost:3002/suites/${form.value.id}`, {
                nbRooms: form.value.nbRooms,
                surface: form.value.surface,
                nbWindows: form.value.nbWindows,
                price: form.value.price,
            });
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

// Remplir le formulaire pour l'édition
const editSuite = (suite) => {
    form.value = { ...suite };
    editMode.value = true;
};

// Supprimer un appartement
const deleteSuite = async (id) => {
    try {
        await axios.delete(`http://localhost:3002/suites/${id}`);
        suites.value = suites.value.filter((suite) => suite.id !== id);
    } catch (error) {
        console.error(error);
    }
};

// Réinitialiser le formulaire après soumission ou annulation
const resetForm = () => {
    form.value = {
        id: null,
        nbRooms: "",
        surface: "",
        nbWindows: "",
        price: "",
    };
    editMode.value = false;
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
</style>
