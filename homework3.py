import math
import random

#input
def getInput():
    numCities = 0
    cities = []
    with open("input.txt", "r") as input:
        for x in input:
            line = x.split()
            if len(line) == 1:
                numCities = int(line[0].replace(",",""))
            else:
                cities.append([int(line[0]), int(line[1]), int(line[2])])
    input.close()
    return numCities, cities

#measure distance
def findDistance(start, end):
    distance = 0.0
    for i in range(len(start)):
        distance += (start[i] - end[i]) ** 2
    return math.sqrt(distance)

def findPathDistance(path):
    distance = 0
    for i in range(len(path)):
        if i == len(path)-1:
            distance += findDistance(path[i], path[0])
        else:
            distance += findDistance(path[i], path[i+1])
    return distance

#create initial pop
def createInitialPopulation(numCities, cities):
    if numCities <= 5:
        popCount = 50
    else:
        popCount = 200    
    population = []
    population.append(cities)
    while len(population) < popCount:
        start = random.randint(0,numCities-1)
        end = random.randint(start, numCities)
        newOrder = population[len(population)-1]
        newOrder = newOrder[end:] + newOrder[start:end] + newOrder[:start]
        population.append(newOrder)
    return population

#order parents
def rankPopulation(paths, distances, bestDistance):
    rankings = []
    totalFitness = 0
    for i in range(len(paths)):
        fitness = (1/distances[i])
        totalFitness += fitness
        rankings.append((i,fitness))
    rankings.sort(key=lambda x: x[1])
    return rankings, totalFitness


#parent selection
def getParents(rankings, totalFitness):
    parentPool = []
    selectionSize = 4
    while len(parentPool) < len(rankings):
        bestParent = (0,0)
        for i in range(selectionSize):
            index = random.randint(0,len(rankings)-1)
            if rankings[index][1] > bestParent[1]:
                bestParent = rankings[index]
        parentPool.append(bestParent[0])
    return parentPool


#crossover
def crossover(parent1, parent2):
    start = random.randint(0,(math.floor(len(parent1)/2)))
    end = random.randint(start,len(parent1)-1)

    child = parent2[:start] + parent1[start:end+1] + parent2[end+1:]

    extra = []
    missing = []
    for i in parent1:
        if i in child:
            index = child.index(i)
            if index < len(child)-1 and i in child[index+1:]:
                extra.append(child.index(i, index+1))
        else:
            missing.append(i)

    if len(missing) > 0:
        for i in range(len(missing)):
            index = extra[i]
            child[index] = missing[i]
    
    return child

def getDistances(population):
    currentBestDistance = math.inf
    currentBestPath = []
    distances = {}
    for i in range(len(population)):
        currentDistance = findPathDistance(population[i])
        distances[i] = currentDistance
        if currentDistance < currentBestDistance:
            currentBestDistance = currentDistance
            currentBestPath = population[i]

    return currentBestDistance, currentBestPath, distances

def mutate(population):
    mutationRate = 0.2
    length = len(population[0])
    mutatedPopulation = []
    for list in population:
        for i in range(int(length*mutationRate)):
            x = random.randint(0,length-1)
            y = random.randint(0,length-1)

            listX = list[x]
            listY = list[y]
            list[x] = listY
            list[y] = listX

        mutatedPopulation.append(list)
    
    return mutatedPopulation

#output
def writeOutput(distance, path):
    with open("output.txt", "w") as output:
        output.write(f"{distance:.3f} \n")
        for location in path:
            output.write(f"{location[0]} {location[1]} {location[2]} \n")
        output.write(f"{path[0][0]} {path[0][1]} {path[0][2]}")
    output.close()

if __name__ == "__main__":
    numCities, cities = getInput()
    population = createInitialPopulation(numCities, cities)   

    bestDistance, bestPath, distances = getDistances(population)
    iterations = 0
    for i in range(5000):
        if i % 1000 == 0: print(i)
        rankings, totalFitness = rankPopulation(population, distances, bestDistance)

        parents = getParents(rankings, totalFitness)

        #breed parents
        children = []
        for j in range(len(parents)):
            parent1 = population[parents[random.randint(0,len(parents)-1)]]
            parent2 = population[parents[random.randint(0,len(parents)-1)]]
            children.append(crossover(parent1, parent2))
        population = children

        if iterations >= 100:
            print("changing it up!")
            population = mutate(population)
            iterations = 0

        newDistance, newPath, distances = getDistances(population)

        if (newDistance < bestDistance):
            bestDistance = newDistance
            bestPath = newPath
            iterations = 0
        else:
            iterations += 1

    writeOutput(bestDistance, bestPath)


