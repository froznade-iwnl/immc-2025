% Distance matrix (5 teams: A=1, B=2, ..., E=5)
distances = [0   500 300 200 400;
            500   0 600 400 300;
            300 600   0 700 500;
            200 400 700   0 800;
            400 300 500 800   0];
teams = {'A', 'B', 'C', 'D', 'E'};
n = length(teams);

% Genetic Algorithm Options
options = optimoptions('ga',...
    'MaxGenerations', 2000,...
    'PopulationSize', 1000,...
    'Display', 'iter');

% Number of unique pairings (n*(n-1) home/away pairs)
num_games = n*(n-1);
num_vars = 2*num_games; % Home and away designations

% Run GA with proper bounds
[solution, fval] = ga(@(x)ttp_fitness(x, distances, n, teams),...
                     num_vars,...
                     [],[],[],[],...
                     ones(1,num_vars),...
                     n*ones(1,num_vars),...
                     [],...
                     1:n,...
                     options);

% Display best schedule
disp_schedule(solution, n, teams);

%% Improved Fitness Function with Duplicate Prevention
function total_dist = ttp_fitness(chromosome, distances, n, teams)
    try
        % Decode chromosome ensuring valid pairings
        [schedule, valid] = decode_schedule(chromosome, n);
        
        if ~valid
            total_dist = 1e9; % Large penalty for invalid schedules
            return;
        end
        
        total_dist = 0;
        
        % Track each team's travel
        team_location = ones(n,1) .* (1:n)'; % Start at home
        
        for round = 1:size(schedule,1)
            home_team = schedule(round,1);
            away_team = schedule(round,2);
            
            % Home team's travel (if they were away last)
            total_dist = total_dist + distances(team_location(home_team), home_team);
            team_location(home_team) = home_team;
            
            % Away team's travel
            total_dist = total_dist + distances(team_location(away_team), home_team);
            team_location(away_team) = home_team;
        end
        
        % Add penalty for constraint violations
        penalty = check_constraints(schedule, n);
        total_dist = total_dist + penalty;
        
    catch
        total_dist = 1e9;
    end
end

%% Constraint Checker with Duplicate Prevention
function penalty = check_constraints(schedule, n)
    penalty = 0;
    
    % 1. Check exactly n-1 home and away games per team
    home_counts = histcounts(schedule(:,1), 1:n+1);
    away_counts = histcounts(schedule(:,2), 1:n+1);
    
    for team = 1:n
        if home_counts(team) ~= n-1 || away_counts(team) ~= n-1
            penalty = penalty + 1e6;
        end
    end
    
    % 2. Check all pairings are unique
    pairings = sort(schedule, 2);
    if size(unique(pairings, 'rows'), 1) ~= n*(n-1)
        penalty = penalty + 1e6;
    end
end

%% Robust Schedule Decoder
function [schedule, valid] = decode_schedule(chromosome, n)
    num_games = n*(n-1);
    schedule = zeros(num_games, 2);
    valid = true;
    
    % Create all possible pairings
    all_pairs = [];
    for i = 1:n
        for j = 1:n
            if i ~= j
                all_pairs = [all_pairs; i j];
            end
        end
    end
    
    % Use chromosome to select pairings
    for i = 1:num_games
        idx = mod(round(chromosome(i)), size(all_pairs,1)) + 1;
        schedule(i,:) = all_pairs(idx,:);
        all_pairs(idx,:) = []; % Remove used pairing
    end
    
    % Final validation
    if any(schedule(:,1) == schedule(:,2))
        valid = false;
    end
end

%% Enhanced Schedule Display
function disp_schedule(solution, n, teams)
    [schedule, valid] = decode_schedule(solution, n);
    if ~valid
        fprintf('Invalid schedule generated\n');
        return;
    end
    
    fprintf('\nValid Tournament Schedule:\n');
    for i = 1:size(schedule,1)
        home = teams{schedule(i,1)};
        away = teams{schedule(i,2)};
        fprintf('Match %2d: %s vs %s\n', i, home, away);
    end
    
    % Verify all pairings
    pairings = sort(schedule, 2);
    unique_pairs = unique(pairings, 'rows');
    if size(unique_pairs,1) == n*(n-1)
        fprintf('\nAll pairings are unique and valid!\n');
    else
        fprintf('\nWarning: Duplicate or invalid pairings exist\n');
    end
end