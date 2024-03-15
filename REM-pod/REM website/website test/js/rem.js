

const baseUrl = "https://rem-pod-app.azurewebsites.net/REM_POD_";


Vue.createApp({
    data() {
        return {
            målinger: [],
            favorites: [],
            idToGetBy: null,
            singleMåling: null,
            addData: { temperature: 0.0, magnetometer: 0.0, distance: 0.0 },
            addMessage: "",
            startTimestamp: '',
            endTimestamp: '',
            filteredMålinger: [],
            temperatureThreshold: 0,
            temperatureSpikesCount: 0,
            temperatureSpikes: [],
        }
    },

    methods: {
        async getAll() {
            try {
                const response = await axios.get(baseUrl);
                if (response.status !== 200) {
                    throw new Error('Network response was not ok.');
                }
                this.målinger = response.data;

            } catch (error) {
                console.error('Error fetching data:', error);
            }
        },

        async getById(id) {
            const url = `${baseUrl}/${id}`;
            try {
                const response = await axios.get(url);
                this.singleMåling = response.data;
            } catch (ex) {
                alert(ex.message + " " + url);
            }
        },

        async addMåling() {
            try {
                this.addData.timeStamp = new Date().toISOString();
                 response = await axios.post(baseUrl, this.addData);
                this.addMessage = `Response ${response.status} ${response.statusText}`;
                this.getAll(); 
            } catch (ex) {
                alert(ex.message);
            }
        },
        async deleteMåling(deleteId) {
            const url =baseUrl +"/" + deleteId
            try{
                response = await axios.delete(url)
                this.deleteMessage = response.status + " " + response.statusText
                this.getAll(0)
            }catch (ex){
                alert(ex.message)
            }
        },
        addToFavorites(item) {
           
            if (!this.isInFavorites(item)) {
              
              this.favorites.push({ ...item });
            }
          },
          removeFromFavorites(favorite) {
            
            const index = this.favorites.findIndex(fav => fav.id === favorite.id);
            if (index !== -1) {
              this.favorites.splice(index, 1);
            }
          },
          isInFavorites(item) {
           
            return this.favorites.some(fav => fav.id === item.id);
          },
        getByTimestampRange() {
            const startTimestamp = new Date(this.startTimestamp).getTime();
            const endTimestamp = new Date(this.endTimestamp).getTime();
    
            this.filteredMålinger = this.målinger.filter(mål => {
                const målTimestamp = new Date(mål.timeStamp).getTime();
                return målTimestamp >= startTimestamp && målTimestamp <= endTimestamp;
            });
        },


        getTemperatureSpikes() {
            this.temperatureSpikes = this.målinger.filter(mål => mål.temperature >= this.temperatureThreshold);
            this.temperatureSpikesCount = this.temperatureSpikes.length;
        },
    },

    mounted() {
        this.getAll();
    }
}).mount("#app");
